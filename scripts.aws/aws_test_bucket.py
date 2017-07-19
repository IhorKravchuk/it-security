#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError
import pprint
import json
import sys
from optparse import OptionParser

__author__ = "Ihor Kravchuk"
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ihor Kravchuk"
__email__ = "igor@it-security.ca"
__status__ = "Development"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = OptionParser()
parser.add_option('-P', '--profile', type='string', dest='aws_profile', help='Please specify AWS CLI profile')
parser.add_option('-B', '--bucket', type='string', dest='bucket', help='Please provide bucket name')

(options, args) = parser.parse_args()

#Parsing comman line input or asking user for missing information
#Checking AWS credentials in profile

if options.aws_profile is None :
    parser.print_help()
    sys.exit(-1)
elif options.bucket is None :
    parser.print_help()
    sys.exit(-1)
else:
    try:
        boto3.setup_default_session(profile_name=options.aws_profile)
    except:
        print bcolors.FAIL+ "Your credentials in the profile (", options.aws_profile, " ) do not allow AWS access"+bcolors.ENDC
        parser.print_help()
        sys.exit(-1)




s3=boto3.client('s3')
try:
    response = s3.get_object(
        Bucket=options.bucket,
        Key='index.html',
    )
    print bcolors.WARNING+ "Bucket: "+ options.bucket+ bcolors.ENDC+ " - Found index.html, most probably S3 static web hosting is enabled"
except ClientError as ex:
#    print ex
#    print ex.response
    if ex.response['Error']['Code'] == "NoSuchBucket":
        print bcolors.OKGREEN+ "Bucket: "+ options.bucket+ bcolors.ENDC+ " - "+ ex.response['Error']['Message']
    elif ex.response['Error']['Code'] == "AccessDenied":
        print bcolors.OKBLUE+ "Bucket: "+ options.bucket+ bcolors.ENDC+ " - Bucket exists, but "+ ex.response['Error']['Message']
    elif ex.response['Error']['Code'] == "NoSuchKey":
        print bcolors.FAIL+ "Bucket: "+ options.bucket+ bcolors.ENDC+ " - Bucket exists, publicly available and no S3 static web hosting, most probably misconfigured! "
