#!/usr/bin/python

import boto3
import pprint
import sys
import json
from optparse import OptionParser
import progressbar as pb


__author__ = "Ihor Kravchuk"
__license__ = "GPL"
__version__ = "2.0.0"
__maintainer__ = "Ihor Kravchuk"
__email__ = "igor@it-security.ca"
__status__ = "Development"

# menu function - creates simple numbered menu and returns user's choice
def menu(items, message):
    print "\n"
    for  index, item in enumerate(items):
        if encryption_enforced(item):
            print index,") ", item, bcolors.OKGREEN + "Encryption enforced: Yes" + bcolors.ENDC
        else:
            print index,") ", item, bcolors.WARNING + "Encryption enforced: NO" + bcolors.ENDC
    return int(raw_input(message))

# Checking if encryption is enforced on the bucket level
def encryption_enforced(bucket_name):
    client = boto3.client('s3')
    try:
        bucket_policy = client.get_bucket_policy(Bucket=bucket_name)
        bucket_policy_j = json.loads(bucket_policy["Policy"])
#        print json.dumps(bucket_policy_j, indent=4, sort_keys=True)
        enc_enforced = False
        for statement in bucket_policy_j["Statement"]:
            if (statement["Action"] == "s3:PutObject" and
                statement.get("Condition") != None and
                statement["Effect"] == "Deny"):
                if "s3:x-amz-server-side-encryption" in statement["Condition"].get("StringNotEquals"):
                    enc_enforced = True
                    break
    except:
        enc_enforced = False
    return enc_enforced

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
parser.add_option('-B', '--bucket', type='string', dest='bucket_name', help='Please specify bucket name')
parser.add_option('-P', '--profile', type='string', dest='aws_profile', default="default", help='Please specify AWS CLI profile')
parser.add_option('-F', '--file', type='string', dest='results_file',  help='Optional: Specify file to save results')

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
# Getting bucket name from user or from cli options
if options.bucket_name is  None :
    try:
        s3 = boto3.resource('s3')
        bucket_iterator = s3.buckets.all()
        buckets_list = [bucket.name for bucket in bucket_iterator]
        bucket_name = buckets_list[menu(buckets_list, "Please choose a bucket to scan : ")]
        print "Bucket to be scanned: "+ bcolors.WARNING + bucket_name +bcolors.ENDC
    except:
        parser.print_help()
        print bcolors.FAIL+ "Your credentials in profile (", options.aws_profile, ") do not grant access to the buckets"+bcolors.ENDC
        sys.exit(-1)
else:
    bucket_name = options.bucket_name
# Print Encryption policy status for the bucket
    if encryption_enforced(bucket_name):
        print bcolors.OKGREEN + "This bucket has encryption enforced for the objects upload " +bcolors.ENDC
    else:
        print bcolors.FAIL + "This bucket has NO encryption enforced" +bcolors.ENDC


# Analising bucket content

#initialize widgets
widgets = ['Scanning S3 bucket ', pb.Percentage(), ' ',
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]

# Getting total number of objects in the bucket
try:
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    print bcolors.BOLD + "Bucket Scan started " +bcolors.ENDC
    bucket_content = bucket.objects.all()
    total_objects = len(list(bucket_content))
except:
    parser.print_help()
    print "Wrong bucket name or credentials in your profile ", options.aws_profile, " do not grant access to the bucket", bucket_name
    sys.exit(-1)
print "Total number of objects in the bucket: ", total_objects

#initialize timer and counters
timer = pb.ProgressBar(widgets=widgets, maxval=total_objects).start()
i=0
not_encrypted =[]

# Looking for each object properties
for obj in bucket_content:
    key = s3.Object(bucket.name, obj.key)
# Amout of the objects in the bucket could increase during s3 bucket audit casuing timer going out of range
    if i < total_objects:
         timer.update(i)
         i+=1
    if key.server_side_encryption is None:
        not_encrypted.append(key)
timer.finish()


#  Result summary
print bcolors.WARNING +"We have found :  ", len(not_encrypted), " NOT encrypted objects"+bcolors.ENDC , " out of total of ",total_objects, " objects in the Bucket"

# Suggesting to save results
if options.results_file is None:
    results_file = raw_input('Please, provide file name to save results or hit Enter to ingore: ')
else:
    results_file = options.results_file

# Saving or printing results
if not results_file:
    for s3_nc_key in not_encrypted:
        print bcolors.WARNING +"Not encrypted object found: " +bcolors.ENDC, s3_nc_key
    sys.exit(0)
else:
    with open(results_file, 'w+') as f:
        f.writelines("%s \n" % str(s3_nc_key) for s3_nc_key in not_encrypted)
    print "Done"
