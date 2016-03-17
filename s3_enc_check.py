#!/usr/bin/python

import boto3
import pprint
import sys
from optparse import OptionParser
import progressbar as pb


__author__ = "Ihor Kravchuk"
__license__ = "GPL"
__version__ = "1.1.0"
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
parser.add_option('-B', '--bucket', type='string', dest='bucket_name', help='Please specify bucket name')
parser.add_option('-P', '--profile', type='string', dest='aws_profile', default="default", help='Please specify AWS CLI profile')
parser.add_option('-F', '--file', type='string', dest='results_file',  help='Optional: Specify file to save results')

(options, args) = parser.parse_args()

if options.bucket_name is  None :
    parser.print_help()
    sys.exit(-1)
if options.aws_profile is None :
    parser.print_help()
    sys.exit(-1)


#initialize widgets
widgets = ['Scanning S3 bucket ', pb.Percentage(), ' ',
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]

try:
    boto3.setup_default_session(profile_name=options.aws_profile)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(options.bucket_name)
    bucket_content = bucket.objects.all()
    total_objects = len(list(bucket_content))
except:
    parser.print_help()
    print "Wrong bucket name or your credentials in profile ", options.aws_profile, " do not grant access to the bucket", options.bucket_name
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
    results_file = raw_input('Please, provide file name to save results or hit Enter to ignore: ')
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
