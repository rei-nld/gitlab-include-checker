resource "aws_s3_object" "package" {
  bucket = resource.aws_s3_bucket.largest_graveyard_mmxxiv.bucket
  key    = "package.zip"
  source = "./package.zip"
}