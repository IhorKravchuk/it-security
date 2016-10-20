# it-security
it-security related scripts and tools

---
### aws_secgroup_viewer .py
Almost any AWS CloudFormation template are more then long enough. It's OK when you are dealing with different relatively "static" resources but become a big  problem for something way more dynamic like security group.

This kind of resource you need to modify and review a lot, especially if you cloud security professional.  Reading AWS CloudFromation template JSON manually  makes your life miserable and you can easily miss bunch of security problems and holes.

My small aws_secgroup_viewer Python program helps you to quickly review and analyze all security groups in your template.

Supports both security group notations used by CloudFormation: firewall rules inside security group or as separate resources linked to group.

### s3_enc_check.py

You have existing S3 bucket with data uploaded before you enable this policy, you have mixed (encrypted and non encrypted objects) or just doing security audit. In this case you need to scan the bucket to find unencrypted objects. How? quite easy using  few python lines bellow:

```
import boto3
import pprint
import sys

boto3.setup_default_session(profile_name='prod')
s3 = boto3.resource('s3')
if len(sys.argv) < 2:
   print "Missing bucket name"
   sys.exit
bucket = s3.Bucket(sys.argv[1])
for obj in bucket.objects.all():
   key = s3.Object(bucket.name, obj.key)
   if key.server_side_encryption is None:
       print "Not encrypted object found:", key
```



Nice, Yep, But it will take almost forever to scan bucket that contains thousand or tens of thousand of objects. In this it would be nice to have some counters, progress bar, ETA , summary, etc.. So, vuala:


Small program providing all these features mentioned. Feel free to use it or request reasonable changes/modifications.

---
### Self-Defending Cloud PoC or Amazon CloudWatch Events usage

PoC of the Self-Defending Cloud concept described in this blog post:
http://security-ingvar-ua.blogspot.ca/2016/10/self-defending-cloud-poc-or-amazon.html

Files needed:
selfdefence.infosec.vpc.json
selfdefence_infosec.py

To deploy you need:
1. selfdefence.infosec.vpc.json - template itself.
2. selfdefence_infosec.py - Lambda function. You will need to Zip it and upload to the s3 bucket with versioning enabled.
3. Edit template (selfdefence.infosec.vpc.json) and specify: S3 bucket name in format you.bucket.name.env.cloudform (where env - is your environment name: prod, test, staging, etc) and S3 version for  selfdefence_infosec.zip file.
4. upload template to the same s3 bucket.
5. Create a stack using this template end specify corresponding environment name at the creation time.

Enjoy!
