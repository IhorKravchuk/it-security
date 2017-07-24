#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError
import pprint
import json
import sys
from optparse import OptionParser
from termcolor import colored, cprint

__author__ = "Ihor Kravchuk"
__license__ = "GPL"
__version__ = "0.3.0"
__maintainer__ = "Ihor Kravchuk"
__email__ = "igor@it-security.ca"
__status__ = "Development"

# Cheking black box bucket security status
def check_bucket(bucket_name):
    # Trying to retrive index.html from the bucket
    try:
        response = s3.get_object(Bucket=bucket_name, Key='index.html')
        bucket_status_code = "S3WebSite"
    except ClientError as ex:
    #    print ex.response
        bucket_status_code= ex.response['Error']['Code']
    return bucket_status_code

# Cheking Authenticated bucket security status
def check_auth_bucket(bucket_name):
# Let's check S3 static web site hosting status
    try:
        website_status =s3.get_bucket_website(Bucket=bucket_name)
        bucket_status_code = "S3WebSite!"
        return bucket_status_code
    except ClientError as ex:
        bucket_status_code = ex.response['Error']['Code']
# Let's try to get bucket ACL and Policy
# ACL
    try:
        bucket_acl = s3.get_bucket_acl(Bucket=bucket_name)
        for grant in bucket_acl["Grants"]:
            if grant["Grantee"]["Type"] == "Group" and "AllUsers" in grant["Grantee"].get("URI"):
                bucket_status_code = "AllUsersAccess"
                return bucket_status_code
            elif grant["Grantee"]["Type"] == "Group" and "AuthenticatedUsers" in grant["Grantee"].get("URI"):
                bucket_status_code = "AllAuthUsersAccess"
                return bucket_status_code

    except ClientError as ex:
        if ex.response['Error']['Code'] == "AccessDenied":
            bucket_status_code = "AccessDenied2ACL"
        else:
            bucket_status_code ="Can'tVerify"
            # cprint ("Weird"+ str(ex.response['Error']), "red")
#Policy
    try:
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        bucket_policy_j = json.loads(bucket_policy["Policy"])
        for statement in bucket_policy_j["Statement"]:
            if (statement.get("Condition") is None and
                statement["Effect"] == "Allow" and
                ("'*'" in str(statement["Principal"]) or statement["Principal"] == "*")):
                bucket_status_code = str(statement["Action"])
                return bucket_status_code
# Policy exists but not allow public access
        bucket_status_code = "NoPublicAccess"
    except ClientError as ex:
        if ex.response['Error']['Code'] == "NoSuchBucketPolicy":
            bucket_status_code = "NoSuchBucketPolicy"
        elif ex.response['Error']['Code'] == "AccessDenied":
            bucket_status_code = "AccessDenied2Policy"

        else:
            bucket_status_code ="Can'tVerify"
            # cprint("Weird"+ str(ex.response['Error']), "red")
#   return status code
    return bucket_status_code


def print_bucket_status(bucket, status):
# Public access exists
    if status == "S3WebSite":
        print colored("Bucket: "+ bucket, color="yellow"), " - Found index.html, most probably S3 static web hosting is enabled"
    elif status == "S3WebSite!":
        print colored("Bucket: "+ bucket, color="yellow"), " - S3 static web hosting is enabled on the bucket"
    elif status == "NoSuchKey":
        print colored("Bucket: "+ bucket, color="red"),  " - Bucket exists, publicly available and no S3 static web hosting, most probably misconfigured! "
    elif status == "AllUsersAccess" or status == "AllAuthUsersAccess":
        print colored("Bucket: "+ bucket, color="red"),  " - Bucket exists and publicly ( "+ status+ " ) "+  " available. Reason: Bucket ACL ! "
    elif "s3:" in status:
        print colored("Bucket: "+ bucket, color="red"),  " - Bucket exists and publicly ( "+ status+ " ) "+  " available. Reason: Bucket Policy ! "
# Can't check due to the access restrictions:
    elif status == "AccessDenied2ACL" or status == "AccessDenied2Policy":
        print colored("Bucket: "+ bucket, color="yellow"),  " - Bucket exists, but can't verify policy or ACL due to the: "+ status
# No public acess
    elif status == "AccessDenied" or status == "NoSuchBucketPolicy" or status == "NoPublicAccess":
        print colored("Bucket: "+ bucket, color="green"), " - No public access detected"
# No bucket - no problem
    elif status == "NoSuchBucket":
        print colored("Bucket: "+ bucket, color="green"),  " - The specified bucket does not exist"
# Can't really verify due to the API Error
    elif status == "Can'tVerify" or status == "InvalidRequest":
        print colored("Bucket: "+ bucket, color="yellow"),  "- Can't really verify due to the API Error"
    else:
        cprint("Bucket: "+ bucket+ "----"+ status, "yellow")
    return

parser = OptionParser()
parser.add_option('-P', '--profile', type='string', dest='aws_profile', help='Please specify AWS CLI profile')
parser.add_option('-B', '--bucket', type='string', dest='bucket', help='Please provide bucket name')
parser.add_option('-F', '--file', type='string', dest='file', help='Optional: file with bucket list to check')

(options, args) = parser.parse_args()

#seting some variables
buckets = set()
buckets_statuses = {}

#Parsing comman line input or asking user for missing information
if options.aws_profile is None :
    parser.print_help()
    sys.exit(-1)
elif options.bucket is None and options.file is None:
    parser.print_help()
    sys.exit(-1)
else:
    try:
#Checking AWS credentials in profile
        boto3.setup_default_session(profile_name=options.aws_profile)
    except:
        cprint("Your credentials in the profile ("+ options.aws_profile+ " ) do not allow AWS access", color="red")
        parser.print_help()
        sys.exit(-1)

# Batch mode: working with files

if options.file is not None and options.file != "aws":
    content = open(options.file, "r")
    for s3bucket in content:
        buckets.add(s3bucket.strip())
    content.close()
else: buckets.add(options.bucket)

# Getting list of the buckets in the account provided to choose scan mode:
try:
    s3res = boto3.resource('s3')
    bucket_iterator = s3res.buckets.all()
    buckets_in_account = set([bucket.name for bucket in bucket_iterator])
except:
    cprint("Your credentials in the profile ("+ options.aws_profile+ " ) do not allow access to enumerate buckets", color="red")
    parser.print_help()
    sys.exit(-1)

# Own account mode, getting list of buckets in the account

if options.bucket is  None  and options.file == "aws":
    buckets = buckets_in_account

s3=boto3.client('s3')

# Cheking bucket statuses
for bucket in buckets:
    print "Checking bucket: "+bucket
#Choosing what scan to perform
    if bucket in buckets_in_account:
        buckets_statuses[bucket] = check_auth_bucket(bucket)
    else:
        buckets_statuses[bucket] = check_bucket(bucket)
#    print_bucket_status(bucket, buckets_statuses[bucket])

# Printing sorted results
for bucket, buckets_status in sorted(buckets_statuses.iteritems(), key=lambda (k,v): (v,k)):
    print_bucket_status(bucket, buckets_status)
