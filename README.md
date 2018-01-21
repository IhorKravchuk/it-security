# it-security
it-security related scripts and tools

## Folder: scripts.aws

### aws_test_bucket.py
Auditing AWS account you have full access to is quite easy - just list the buckets and check theirs ACL, users and buckets' policies via aws cli or web gui.

What about cases when you:
* have many accounts and buckets (will take forever to audit manually)
* do not have enough permissions in the target AWS account to check bucket access
* you do not have permissions at all in this account (pentester mode)

To address everything above I've created small tool to do all dirty job for you:


```
$python aws_test_bucket.py --profile prod-read --bucket test.bucket
$python aws_test_bucket.py --profile prod-read --file aws
$python aws_test_bucket.py --profile prod-read --file buckets.list

  -P AWS_PROFILE, --profile=AWS_PROFILE
                        Please specify AWS CLI profile
  -B BUCKET, --bucket=BUCKET
                        Please provide bucket name
  -F FILE, --file=FILE  Optional: file with buckets list to check or aws to check all buckets in your account

```
**Note:**
*--profile=AWS_PROFILE - yours AWS access profile (from aws cli). This profile  might or might not have access to the audited bucket (we need this just to become Authenticated User from AWS point of view ).*

If  AWS_PROFILE allows authorized access to the bucket being audited - tool will fetch bucket's ACLs, Policies and S3 Static Web setting and perform authorized audit.

If AWS_PROFILE does not allow authorized access - tool will work in pentester mode

You can specify:
 * one bucket to check using **--bucket** option
 * file with list of buckets(one bucket name per line) using **--file** option
 * all buckets in your AWS account (accessible using AWS_PROFILE) using **--file=aws** option


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

### aws_secgroup_viewer .py
Almost any AWS CloudFormation template are more then long enough. It's OK when you are dealing with different relatively "static" resources but become a big  problem for something way more dynamic like security group.

This kind of resource you need to modify and review a lot, especially if you cloud security professional.  Reading AWS CloudFromation template JSON manually  makes your life miserable and you can easily miss bunch of security problems and holes.

My small aws_secgroup_viewer Python program helps you to quickly review and analyze all security groups in your template.

Supports both security group notations used by CloudFormation: firewall rules inside security group or as separate resources linked to group.

----

## Folders: tf and cf

More details described in these blog posts

**Updated** version with Terraform integration: http://blog.it-security.ca/2018/01/secure-your-aws-account-using-terrafrom.html

Initial version: http://blog.it-security.ca/2016/11/secure-your-aws-account-using.html


### Secure your AWS account using Terraform and  CloudFormation

The very first thing you need to do while building your AWS infrastructure is to enable and configure all AWS account level security features such as: CloudTrail, CloudConfig, CloudWatch, IAM, etc..
To do this, you can use mine Amazon AWS Account level security checklist and how-to or any other source.
To avoid manual steps and to be align with SecuityAsCode concept, I use Terraform and set of CloudFormation templates, simplified version of which described below. Now, it's
1. integrated with Terraform (use terraform templates in the folder **tf**)
2. creates prerequisites for Splunk integration (User, key, SNS, and SQS)
3. configures cross account access (for multiaccounts organizations, adding ITOrganizationAccountAccessRole with MFA enforced)
4. implements Section 3 (Monitoring) of the **CIS Amazon Web Services Foundations benchmark.**
5. configures CloudTrail according to the new best practices (KMS encryption, validation etc)
6. Configure basic set of the CloudConfig rules to monitor best practices


#### Global Security stack template structure:

**security.global.yaml** - parent template for all nested templates to link them together and control dependency between nested stacks.

**cloudtrail.clobal.json** - nested template for Global configuration of the CloudTrail

**cloudtrailalarms.global.json** - nested template for Global CloudWatch Logs alarms and security metrics creation. Uses FilterMap to create different security-related filters for ClouTrail LogGroup, corresponding metrics and notifications for suspicious or dangerous events. You can customise filter per environment basis.

**awsconfig.global.json** - nested template for Global AWS Config Service configuration and config rules.

**iam.global.json** - nested template for IAM Global configuration.


#### Supported features:
Environments and regions: Stack designed to cover all AWS account, but to be deployed in only one region. To deploy specify account nick-name and company name (these will be used to create unique s3 buckets names )
AWS services used by stack: CloudTrail, AWS Config, CloudWatch, CloudWatch Logs and Events, IAM.

#### To deploy:

1. Get code from my git repo.
2. Update terraform.tfvars specifying: your AWS profile name (configured for aws cli using aws configure --profile profile_name); name for the environment (prod, test, dev ..) ; company(or division) name; region and AWS master account ID.
3. terraform init to get aws provider downloaded by terraform
4. terraform plan
5. terraform apply




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
