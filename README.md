# it-security
it-security related scripts and tools

---
### aws_secgroup_viewer .py
Almost any AWS CloudFormation template are more then long enough. It's OK when you are dealing with different relatively "static" resources but become a big  problem for something way more dynamic like security group.

This kind of resource you need to modify and review a lot, especially if you cloud security professional.  Reading AWS CloudFromation template JSON manually  makes your life miserable and you can easily miss bunch of security problems and holes.

My small aws_secgroup_viewer Python program helps you to quickly review and analyze all security groups in your template.

Supports both security group notations used by CloudFormation: firewall rules inside security group or as separate resources linked to group.

---
