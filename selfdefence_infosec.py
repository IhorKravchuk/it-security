#!/usr/bin/python

import json
import boto3
import zlib
import base64

def lambda_handler(event, context):
    print event
# analyzing event
    if event['detail']['requestParameters'].get('disableApiTermination')!= None:
        protection_status = event['detail']['requestParameters']['disableApiTermination']['value']
        UserName = event['detail']['userIdentity']['userName']
        UserID = event['detail']['userIdentity']['principalId']
        if event['detail']['userIdentity'].get('sessionContext') != None:
            mfa = event['detail']['userIdentity']['sessionContext']['attributes']['mfaAuthenticated']
        else:
            mfa = "false"
        print protection_status, UserName, UserID, mfa
# disabling user using inline user policy if no MFA being used
        if mfa != "true" and not protection_status:
            iam = boto3.resource('iam')
            user_policy = iam.UserPolicy(UserName,'disable_user')
            response = user_policy.put(PolicyDocument='{ "Version": "2012-10-17", "Statement": [{"Sid": "Disableuser01","Effect": "Deny","Action": ["ec2:StopInstances", "ec2:TerminateInstances"],"Resource": ["*"]}]}')
            print response


# # to test execution on local computer
# content = open("test_termination_protection_event.json", "r")
# data = content.read()
# content.close()
# # loading JSON
# js = json.loads(data)
#
#
# lambda_handler(js, "test")
