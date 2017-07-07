# it-security
it-security related scripts and tools

## Folder: scripts.aws

### aws_secgroup_viewer .py
Almost any AWS CloudFormation template are more then long enough. It's OK when you are dealing with different relatively "static" resources but become a big  problem for something way more dynamic like security group.

This kind of resource you need to modify and review a lot, especially if you cloud security professional.  Reading AWS CloudFromation template JSON manually  makes your life miserable and you can easily miss bunch of security problems and holes.

My small aws_secgroup_viewer Python program helps you to quickly review and analyze all security groups in your template.

Supports both security group notations used by CloudFormation: firewall rules inside security group or as separate resources linked to group.

----
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

### aws_enforce_password_policy.py

Small tool to check or/and enforce passsword policy on AWS account. Handy when you need to do this in many AWS accounts.

----

## Folder: security.global.cf

### Secure your AWS account using CloudFormation

The very first thing you need to do while building your AWS infrastructure is to enable and configure all AWS account level security features such as: CloudTrail, CloudConfig, CloudWatch, IAM, etc..
To do this, you can use mine Amazon AWS Account level security checklist and how-to or any other source.
To avoid manual steps and to be align with SecuityAsCode concept, I use set of CloudFormation templates, simplified version of which I would like to share:


#### Global Security stack template structure: More details described in this blog post:
http://security-ingvar-ua.blogspot.ca/2016/11/secure-your-aws-account-using.html

**security.global.json** - parent template for all nested templates to link them together and control dependency between nested stacks.

**cloudtrail.clobal.json** - nested template for Global configuration of the CloudTrail

**cloudtrailalarms.global.json** - nested template for Global CloudWatch Logs alarms and security metrics creation. Uses FilterMap to create different security-related filters for ClouTrail LogGroup, corresponding metrics and notifications for suspicious or dangerous events. You can customise filter per environment basis.

**awsconfig.global.json** - nested template for Global AWS Config Service configuration.

**cloudwatchsubs.global.json** - nested template for configuring AWS CloudWatch Subscription Filter to extract and analyse most severe CloudTrail events using custom Lambda function.

**iam.global.json** - nested template for IAM Global configuration.

**cloudwatchsubs_kinesis.global.json** - PoC template (not linked as nested to the security.global.json)  for configuring AWS CloudWatch Subscription Filter to send most severe CloudTrail events to AWS Kinesis stream using subscription filter similar to the cloudwatchsubs.global.json

#### Supported features:
Environments and regions: Stack supports unlimited amount of environments with 4 environments predefined (staging, dev, prod, and dr) and use 1 account and 1 region per environment concept to reduce blast radius (if account become compromised)
AWS services used by stack: CloudTrail, AWS Config, CloudWatch, CloudWatch Logs and Events, IAM,  Lambda, Kinesis.

#### To deploy:

1. Create bucket using following naming convention: com.ChangeMe.EnviromentName.cloudform, replacing ChangeMe and EnviromentName with your value to make it look like this: com.it-security.prod.cloudform
2. Enable bucket versioning
3. in the templates  security.global.json and cloudwatchsubs.global.json replace "ChangeMe" with name used in the bucket creation.
4. In the template cloudtrailalarms.global.json modify SNS endpoints for email notification infosec@ChangeMe.com and devops@ChangeMe.com; Add endpoints with mobile phone numbers for SMS notification to appropriate SNS topics if needed.
5. Modify iam.global.json template to adrress you SQL DataBase bucket location (com-ChangeMe-", {"Ref": "Environment"} , "-sqldb/)  and modify any permission if need according to your organisation structure, roles, responsibilities and services.
6. Modify FilterMap in cloudtrailalarms.global.json and cloudwatchsubs.global.json templates make filters work for your infrastructure (Critical Instance IDs, Critical Volume IDs, you ofiice IP range, you NAT gateways, etc)
7. Zip example Lambda function LogCritical_lambda_security_global.py like LogCritical_lambda_security_global.zip
8. Upload this function into S3 bucket created at step 1 and copy object version (GUI- show version -object properties ) and insert into cloudwatchsubs.global.json template into "LogCriticalLambdaCodeVer" mapping at the appropriate environment (prod, staging ..)
9. Modify "regions" Environments mapping in the iam.global.json, and cloudwatchsubs.global.json templates to specify correct AWS region you are using for the deployment.
10. Upload all .global.json templates into S3 bucket created at step 1.
11. Create new CloudFormation stack  using parent security template security.global.json and your bucket name (Example: ttps://s3.amazonaws.com/com.it-security.prod.cloudform/security.global.json ),  call it "Security" and specify environment name you going to deploy.
12. Done!

---
## Folder: selfdefence.PoC.cf

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
