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
__version__ = "0.2.0"
__maintainer__ = "Ihor Kravchuk"
__email__ = "igor@it-security.ca"
__status__ = "Development"

# Cheking bucket security status
def check_bucket(bucket_name):
    try:
        response = s3.get_object(
            Bucket=bucket_name,
            Key='index.html',
        )
        bucket_status_code = "S3WebSite"
    except ClientError as ex:
    #    print ex
    #    print ex.response
        bucket_status_code= ex.response['Error']['Code']
    return bucket_status_code

def print_bucket_status(bucket, status):
    if status == "S3WebSite":
        print colored("Bucket: "+ bucket, color="yellow"), " - Found index.html, most probably S3 static web hosting is enabled"
    elif status == "NoSuchBucket":
        print colored("Bucket: "+ bucket, color="green"),  " - The specified bucket does not exist"
    elif status == "AccessDenied":
        print colored("Bucket: "+ bucket, color="blue"), " - Bucket exists, but Access Denied"
    elif status == "NoSuchKey":
        print colored("Bucket: "+ bucket, color="red"),  " - Bucket exists, publicly available and no S3 static web hosting, most probably misconfigured! "
    return

parser = OptionParser()
parser.add_option('-P', '--profile', type='string', dest='aws_profile', help='Please specify AWS CLI profile')
parser.add_option('-B', '--bucket', type='string', dest='bucket', help='Please provide bucket name')
parser.add_option('-F', '--file', type='string', dest='file', help='Optional: file with bcuket list to check')

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

if options.file is not None:
    content = open(options.file, "r")
    for s3bucket in content:
        buckets.add(s3bucket.strip())
    content.close()
else: buckets.add(options.bucket)


s3=boto3.client('s3')

# Cheking bucket statuses
for bucket in buckets:
    buckets_statuses[bucket] = check_bucket(bucket)
#    print_bucket_status(bucket, buckets_statuses[bucket])
#print buckets_statuses

# Printing sorted results
for bucket, buckets_status in sorted(buckets_statuses.iteritems(), key=lambda (k,v): (v,k)):
    print_bucket_status(bucket, buckets_status)




# try:
#     response = s3.get_object(
#         Bucket=options.bucket,
#         Key='index.html',
#     )
#     print colored("Bucket: "+ options.bucket, color="yellow"), " - Found index.html, most probably S3 static web hosting is enabled"
# except ClientError as ex:
# #    print ex
# #    print ex.response
#     if ex.response['Error']['Code'] == "NoSuchBucket":
#         print colored("Bucket: "+ options.bucket, color="green"),  " - "+ ex.response['Error']['Message']
#     elif ex.response['Error']['Code'] == "AccessDenied":
#         print colored("Bucket: "+ options.bucket, color="blue"), " - Bucket exists, but "+ ex.response['Error']['Message']
#     elif ex.response['Error']['Code'] == "NoSuchKey":
#         print colored("Bucket: "+ options.bucket, color="red"),  " - Bucket exists, publicly available and no S3 static web hosting, most probably misconfigured! "
