
### Secure your AWS account using CloudFormation

The very first thing you need to do while building your AWS infrastructure is to enable and configure all AWS account level security features such as: CloudTrail, CloudConfig, CloudWatch, IAM, etc..
To do this, you can use mine Amazon AWS Account level security checklist and how-to or any other source.
To avoid manual steps and to be align with SecuityAsCode concept, I use set of CloudFormation templates, simplified version of which described below. Now, it's
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
