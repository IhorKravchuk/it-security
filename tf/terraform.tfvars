#--------------------------------------------------------------
# General
#--------------------------------------------------------------
#Replace it-secuity and master_account # with corresponding to your comapny data
aws_profile  	= "it-security"
enviroment_name = "prod"
company_name 	= "it-security"
region          = "us-east-1"
# Master account for AWS cross account access (using ITOrganizationAccountAccessRole with MFA enforced)
master_account  = "1234566789"

#--------------------------------------------------------------
# Network
#--------------------------------------------------------------
# Office
# Please specify you office external IP range (for future use)
rp_cidr           = "172.0.0.1/24"

# VPC
vpc_cidr          = ""

# Instances Subnets
private_subnets   = ""
public_subnets    = ""
protected_subnets = ""


#--------------------------------------------------------------
# Instances
#--------------------------------------------------------------

# CentOS 6 (x86_64) - with Updates HVM
# https://aws.amazon.com/marketplace/pp/B00NQAYLWO?qid=1489159620460&sr=0-2&ref_=srh_res_product_title
centos_6_ami.ca-central-1   = "ami-b17cced5"  # Canada (Central)
centos_6_ami.us-east-1      = "ami-1c221e76"  # US East (N. Virginia)
centos_6_ami.us-east-2      = "ami-c299c2a7"  # US East (Ohio)
centos_6_ami.us-west-1      = "ami-ac5f2fcc"  # US West (N. California)
centos_6_ami.us-west-2      = "ami-05cf2265"  # US West (Oregon)
centos_6_ami.eu-central-1   = "ami-2bf11444"  # EU (Frankfurt)
centos_6_ami.eu-west-1      = "ami-edb9069e"  # EU (Ireland)
centos_6_ami.eu-west-2      = "ami-ba373dde"  # EU (London)
centos_6_ami.ap-southeast-1 = "ami-106aa373"  # Asia Pacific (Singapore)
centos_6_ami.ap-southeast-2 = "ami-87d2f4e4"  # Asia Pacific (Sydney)
centos_6_ami.ap-northeast-1 = "ami-fa3d3f94"  # Asia Pacific (Tokyo)
centos_6_ami.ap-northeast-2 = "ami-56478938"  # Asia Pacific (Seoul)
centos_6_ami.ap-south-1     = "ami-9b1c76f4"  # Asia Pacific (Mumbai)
centos_6_ami.sa-east-1      = "ami-03b93b6f"  # South America (Sao Paulo)
