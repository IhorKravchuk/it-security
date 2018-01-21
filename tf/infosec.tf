# Enviroment targeting

variable "aws_profile" { }
variable "enviroment_name" { }
variable "company_name" { }
variable "master_account" { }
variable "region" { default = "us-east-1" }

# Template names
variable "path_to_cf" { default=  "../cf/security.global.cf/" }
variable "security_global" { default = "security.global.yaml" }
variable "cloudtrail_global" { default = "cloudtrail.global.json" }
variable "awsconfig_global" { default = "awsconfig.global.json" }
variable "cloudtrailalarms_global" { default = "cloudtrailalarms.global.json" }
variable "iam_global" { default = "iam.global.json" }


variable "azs" {
  type = "map"
  default = {
    "0" = "c"
    "1" = "d"
  }
}


provider "aws" {
  region = "${var.region}"
  profile = "${var.aws_profile}"
}

#--------------------------------------
# Creating Security Clouformation stack
#--------------------------------------

# s3 bucket for cloudformation template

resource "aws_s3_bucket" "CFbucket" {
    bucket = "com.${var.company_name}.${var.enviroment_name}.cloudform"
    acl = "private"
    versioning {
          enabled = true
        }
    lifecycle_rule {
          id = "global"
          enabled = true
          noncurrent_version_expiration {
          days = 90
          }
        }
}

# uploading CloudFormation template to the bucket

resource "aws_s3_bucket_object" "security_global" {
  bucket = "${aws_s3_bucket.CFbucket.bucket}"
  key    = "${var.security_global}"
  source = "${var.path_to_cf}${var.security_global}"
  etag   = "${md5(file("${var.path_to_cf}${var.security_global}"))}"
}

resource "aws_s3_bucket_object" "cloudtrail_global" {
  bucket = "${aws_s3_bucket.CFbucket.bucket}"
  key    = "${var.cloudtrail_global}"
  source = "${var.path_to_cf}${var.cloudtrail_global}"
  etag   = "${md5(file("${var.path_to_cf}${var.cloudtrail_global}"))}"
}

resource "aws_s3_bucket_object" "awsconfig_global" {
  bucket = "${aws_s3_bucket.CFbucket.bucket}"
  key    = "${var.awsconfig_global}"
  source = "${var.path_to_cf}${var.awsconfig_global}"
  etag   = "${md5(file("${var.path_to_cf}${var.awsconfig_global}"))}"
}

resource "aws_s3_bucket_object" "cloudtrailalarms_global" {
  bucket = "${aws_s3_bucket.CFbucket.bucket}"
  key    = "${var.cloudtrailalarms_global}"
  source = "${var.path_to_cf}${var.cloudtrailalarms_global}"
  etag   = "${md5(file("${var.path_to_cf}${var.cloudtrailalarms_global}"))}"
}

resource "aws_s3_bucket_object" "iam_global" {
  bucket = "${aws_s3_bucket.CFbucket.bucket}"
  key    = "${var.iam_global}"
  source = "${var.path_to_cf}${var.iam_global}"
  etag   = "${md5(file("${var.path_to_cf}${var.iam_global}"))}"
}
# creating Security cloudforation stack

resource "aws_cloudformation_stack" "Security" {
  name = "Security"
  depends_on = ["aws_s3_bucket_object.iam_global", "aws_s3_bucket_object.cloudtrailalarms_global", "aws_s3_bucket_object.awsconfig_global", "aws_s3_bucket_object.cloudtrail_global", "aws_s3_bucket_object.security_global"]
  parameters {
    AccountNickname = "${var.enviroment_name}",
    CompanyName = "${var.company_name}",
    MasterAccount = "${var.master_account}"
  }
  template_url = "https://s3.amazonaws.com/${aws_s3_bucket.CFbucket.bucket}/${var.security_global}?versionId=${aws_s3_bucket_object.security_global.version_id}"
  capabilities = [ "CAPABILITY_NAMED_IAM" ]
  tags { "owner" = "infosec"}
}

# ---------------------------
# Configuring Account Level Password Policy
#----------------------------

resource "aws_iam_account_password_policy" "strict" {
  minimum_password_length        = 14
  require_lowercase_characters   = true
  require_numbers                = true
  require_uppercase_characters   = true
  require_symbols                = true
  allow_users_to_change_password = true
  max_password_age               = 90
  password_reuse_prevention      = 24
}


# ---------------------------
# Configuring Users, policy, keys
#----------------------------



# ---------------------------
# Creating git repos for InfraAsCode
#----------------------------



# ---------------------------
# Building VPCs and Networks
#----------------------------


#--------------------------
# Seting-up Route53 DNS
#--------------------------



#--------------------------
# Seting-up security groups
#--------------------------



#-----------------------
# Building the bastion host
#-----------------------





#-----------------------
# IAM Roles
#-----------------------
