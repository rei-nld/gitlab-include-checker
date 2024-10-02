import os
import csv
import boto3
import requests

GITLAB_API_URL = os.environ['GITLAB_API_URL']
GITLAB_ACCESS_TOKEN = os.environ['GITLAB_ACCESS_TOKEN']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
SES_SENDER = os.environ['SES_SENDER']
SES_RECEIVER = os.environ['SES_RECEIVER']

def lambda_handler(event, context):
    headers = {"Private-Token": GITLAB_ACCESS_TOKEN}
    projects = get_projects(headers)
    results = []

    for project in projects:
        branches = get_branches(headers, project['id'])
        for branch in branches:
            branch_name = branch['name']
            repo_url = project['web_url'] + "/-/tree/" + branch_name
            ci_file = get_file_from_repo(headers, project['id'], '.gitlab-ci.yml', branch_name)
            if ci_file:
                content = ci_file.get('content', '')
                #print("###")
                #print("Start of content of " + project['web_url'] + " : .gitlab-ci.yml in branch " + branch_name)
                #print(content)
                #print("###")
                project_value = extract_project_status(content)
                ref_value = extract_ref_status(content)
                results.append((repo_url, project_value, ref_value))
    upload_results_to_s3(results)
    send_plain_email(results)
    return "Done"

def get_projects(headers):
    response = requests.get(f"{GITLAB_API_URL}/projects", headers=headers)
    response.raise_for_status()
    return response.json()

def get_branches(headers, project_id):
    response = requests.get(f"{GITLAB_API_URL}/projects/{project_id}/repository/branches", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def get_file_from_repo(headers, project_id, file_path, branch='main'):
    encoded_file_path = requests.utils.quote(file_path, safe='')
    response = requests.get(f"{GITLAB_API_URL}/projects/{project_id}/repository/files/{encoded_file_path}/raw?ref={branch}", headers=headers)
    if response.status_code == 200:
        return {"content": response.text}
    return None

def extract_ref_status(content):
    ref_line = next((line for line in content.splitlines() if 'ref:' in line), None)
    if ref_line:
        ref_value = ref_line.split(':', 1)[1].strip()
        return ref_value
    else:
        return "main"
        
def extract_project_status(content):
    project_line = next((line for line in content.splitlines() if 'project:' in line), None)
    if project_line:
        project_value = project_line.split(':', 1)[1].strip()
        return project_value
    else:
        return "undefined"
        
def send_plain_email(content):
    data = "URL,Project,RefValue\n" + "\n".join([f"{url},{projectvalue},{refvalue}" for url, projectvalue, refvalue in content])
    ses_client = boto3.client("ses", region_name="eu-west-3")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                SES_RECEIVER,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": data,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": ".gitlab-ci.yml - Status",
            },
        },
        Source=SES_SENDER,
    )

def upload_results_to_s3(results):
    csv_content = "URL,Project,RefValue\n" + "\n".join([f"{url},{projectvalue},{refvalue}" for url, projectvalue, refvalue in results])
    s3 = boto3.client('s3')
    s3.put_object(Bucket=S3_BUCKET_NAME, Key='gitlab_ci_status.csv', Body=csv_content)

