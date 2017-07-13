#!/usr/bin/python

import boto3
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
parser.add_option('-A', '--action', type='string', dest='action', default="get", help='Please specify action: set or get')

(options, args) = parser.parse_args()

# Parsing comman line input or asking user for missing information
# Checking AWS credentials in profile

if options.aws_profile is None :
    parser.print_help()
    sys.exit(-1)
else:
    try:
        boto3.setup_default_session(profile_name=options.aws_profile)
    except:
        print bcolors.FAIL+ "Your credentials in the profile (", options.aws_profile, " ) do not allow AWS access"+bcolors.ENDC
        parser.print_help()
        sys.exit(-1)

iam=boto3.client('iam')

if options.action == "set" :
    response = iam.update_account_password_policy(
        MinimumPasswordLength=15,
        RequireSymbols=True,
        RequireNumbers=True,
        RequireUppercaseCharacters=True,
        AllowUsersToChangePassword=True,
        RequireLowercaseCharacters=True,
        MaxPasswordAge=90,
        PasswordReusePrevention=24,
        HardExpiry=False
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 :
        print bcolors.OKGREEN+ "Password policy successfully enforced  on the AWS account: "+ str(options.aws_profile) +bcolors.ENDC


print bcolors.OKGREEN+ "Current password policy is: " +bcolors.ENDC
pprint.pprint(iam.get_account_password_policy()["PasswordPolicy"])
