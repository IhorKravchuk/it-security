#!/usr/bin/python

import json
import re
import sys
import os
import pprint
from operator import itemgetter

__author__ = "Ihor Kravchuk"
__license__ = "GPL"
__version__ = "0.9.0"
__maintainer__ = "Ihor Kravchuk"
__email__ = "igor@it-security.ca"
__status__ = "Development"

# command line highlite helper class
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# menu function - creates simple numbered menu and returns user's choice
def menu(items, message):
    print "\n"
    for  index, item in enumerate(items):
        print index,") ", item
    return int(raw_input(message))

def aws_etxract_rules(resource, direction, rule):
    firewall_rule = dict()
    firewall_rule["Direction"] = direction
    try:
        firewall_rule["IpProtocol"] = rule["IpProtocol"]
        if direction == "ingress":
            if rule.get("CidrIp") != None: firewall_rule["Source"] = rule["CidrIp"]
            else: firewall_rule["Source"] = rule["SourceSecurityGroupId"]
        elif direction == "egress":
            if rule.get("CidrIp") != None: firewall_rule["Destination"] = rule["CidrIp"]
            else: firewall_rule["Destination"] = rule["DestinationSecurityGroupId"]
        if firewall_rule["IpProtocol"] == "-1":
            firewall_rule["DestinFromPort"] = "ANY"
            firewall_rule["DestinToPort"] = "ANY"
        else:
            firewall_rule["DestinFromPort"] = rule["FromPort"]
            firewall_rule["DestinToPort"] = rule["ToPort"]
    except:
        print bcolors.WARNING + "---Warning.  Not correct resource description. Missing parameter", resource, " rule: ", str(rule)  + bcolors.ENDC

    return firewall_rule


# Loading data form file
# loading JSON
if len(sys.argv)<2 or not os.path.isfile(sys.argv[1]):
    print "Please specify existing CloudFormation template file name as argument"
    sys.exit(1)
content = open(sys.argv[1], "r")
data = content.read()
content.close()
try:
    js = json.loads(data)
except:
    print "Not a valid JSON file"
    sys.exit(1)


# extracting security groups and firewall rules from JSON and convering it to the IhorFirewallRuleFormat:
# firewall_rule = {"Direction": "ingress/egress", "IpProtocol": "protocol_name", "Source":"CidrIp/sec_group/url", "SourceFromPort":"port", "SourceToPort":"port", "DestinFromPort":"port", "DestinToPort":"port", "Destination":"CidrIp/sec_group/url"}
# security_group = [firewall_rule1, firewall_rule2, firewall_rule3]
# all security groups  = { "sec_group_linux": "security_group", "sec_group_windows": "security_group", "sec_group_oracle": "security_group"}
security_groups = dict()
security_group = list()

# AMAZON CLOUDFORMATION TYPE1
# extracting all firewall rules that defined as a Resources in the template file
for resource in js["Resources"]:
    # Extracting egress and ingress rules
    if js["Resources"][resource]["Type"] == "AWS::EC2::SecurityGroupIngress":
        rule_direction = "ingress"
    elif js["Resources"][resource]["Type"] == "AWS::EC2::SecurityGroupEgress":
        rule_direction = "egress"
    else:
        continue
    try:
        sec_group_name = js["Resources"][resource]["Properties"]["GroupId"]["Ref"]
    except:
        print bcolors.WARNING + "---Warning.  Firewall rule has not security group referenece", resource  + bcolors.ENDC
        continue
    security_groups[sec_group_name] = security_groups.get(sec_group_name, [])
    security_groups[sec_group_name].append(aws_etxract_rules(resource, rule_direction, js["Resources"][resource]["Properties"]))
#print  json.dumps(security_groups, indent=4)


# AMAZON CLOUDFORMATION TYPE2
# extracting all firewall rules that defined as aprt of Security resource in the template file
for resource in js["Resources"]:
    # Extracting Ingress rules inside securuity group
    if js["Resources"][resource]["Type"] == "AWS::EC2::SecurityGroup" and js["Resources"][resource]["Properties"].get("SecurityGroupIngress") != None:
        sec_group_name = resource
        for rule in js["Resources"][resource]["Properties"]["SecurityGroupIngress"]:
            security_groups[sec_group_name] = security_groups.get(sec_group_name, [])
            security_groups[sec_group_name].append(aws_etxract_rules(resource, "ingress", rule))
    if js["Resources"][resource]["Type"] == "AWS::EC2::SecurityGroup" and js["Resources"][resource]["Properties"].get("SecurityGroupEgress") != None:
        sec_group_name = resource
        for rule in js["Resources"][resource]["Properties"]["SecurityGroupEgress"]:
            security_groups[sec_group_name] = security_groups.get(sec_group_name, [])
            security_groups[sec_group_name].append(aws_etxract_rules(resource, "egress", rule))


# User interface
status = 1
while status != 0:
    list_of_groups =security_groups.keys()
    sec_num = menu(list_of_groups, "Enter the number of the security group >> ")
    print "\n Security Group", list_of_groups[sec_num], "\n"
    print bcolors.OKBLUE + "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Direction", "IpProtocol", "Source", "SourceFromPort", "SourceToPort", "DestinToPort", "DestinFromPort", "Destination"  ) + bcolors.ENDC
    sorted_rules = sorted(security_groups[list_of_groups[sec_num]], key=itemgetter('Direction'), reverse=True)
    for rule in sorted_rules:
        print "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(rule.get("Direction"), rule.get("IpProtocol"), rule.get("Source"), rule.get("SourceFromPort"), rule.get("SourceToPort"), rule.get("DestinToPort"), rule.get("DestinFromPort"), rule.get("Destination")  )
    status = menu(["Exit", "Check another security group"], " >> ")
