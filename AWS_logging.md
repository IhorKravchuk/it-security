# Native AWS logging capabilities
official doc (missing a lot of services): https://aws.amazon.com/answers/logging/aws-native-security-logging-capabilities/

[CloudTrail](#cloudtrail)

[CloudWatch Logs](#cloudwatchlogs)


## <a name="cloudtrail"></a> CloudTrail
* Log coverage: 
    * all AWS API calls (covers web-ua, api or SDK actions)
    * List of the services covered by cloudtrail
     https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-aws-service-specific-topics.html
    * Options:
      1. A trail that applies to all regions
      2. A trail that applies to one region
      3. organization trail - global for all subaccount in organization
* Exceptions and Limits:
    * Do not cover newest services/and api calls:
    * List of the uncovered services: 
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-unsupported-aws-services.html
* Log record/file format:
    * json, structure is service-specific
* Delivery latency:
    * Within 15 min of the activity
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
    * S3 bucket
* Encryption at rest:
    * S3 - AES256, S3 SSE with amazon keys or KMS
* Data residency(AWS Region):
    * S3 bucket from any region.
* Retention capabilities:
    * AWS Cloudtrail Console (EventHistory) - 90 days
    * S3 -indefinite time/user defined
    * CloudWatch Logs:  indefinitely and never expire. User can define retention policy per log group (indefinite, or from 1 day to 10years)

## VPC Flow logs
* Log coverage:
    * VPC
    * Subnet
    * Network interface
    * accepted traffic, rejected traffic, or all traffic
    https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
* Exceptions and Limits:

* Log record/file format:
    * space-separated string
    * Format details:
    https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records
* Delivery latency:
    * each capture window: ~10 min
    * max 15 min
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
    * S3 bucket
* Encryption at rest:
    * S3 - AES256, S3 SSE with amazon keys or KMS
* Data residency(AWS Region):
    * S3 bucket from any region.
* Retention capabilities:
    * S3 -indefinite time/user defined
    * CloudWatch Logs:  indefinitely and never expire. User can define retention policy per log group (indefinite, or from 1 day to 10years)


## S3 bucket access logs (S3 Server Logs)

* Log coverage:
    * Logs all requests to the data in the bucket
    * https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html
* Exceptions and Limits:
    * Not guaranteed delivery
* Log record/file format:
    * Newline-delimited log records, Each log record represents one request and consists of space-delimited fields
    * Each access log record provides details about a single access request, such as the requester, bucket name, request time, request action, response status, and an error code, if relevant.
    * https://docs.aws.amazon.com/AmazonS3/latest/dev/LogFormat.html
    * Fields:
        1. Bucket Owner
        2. Bucket
        3. Time
        4. Remote IP
        5. Requester
        6. Request ID
        7. Operation
        8. Key
        9. Request-URI
        10. HTTP status
        11. Error Code
        12. Bytes Sent
        13. Object Size
        14. Total Time
        15. Turn-Around Time
        16. Referrer
        17. User-Agent
        18. Version Id
* Delivery latency:
    * delivered on a best effort basis - normally hours.
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * S3
* Encryption at rest:
    * S3 - AES256, S3 SSE with amazon keys or KMS
* Data residency(AWS Region):
    * Same Region as the source bucket, bucket must be owned by the same AWS account
* Retention capabilities:
    * S3 -indefinite time/user defined

## Elastic Load Balancer(ELB) logs (classic)
* Log coverage:
    * access logs capture detailed information about requests sent to your load balancer. Each log contains information such as the time the request was received, the client's IP address, latencies, request paths, and server responses
    * https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/access-log-collection.html
* Exceptions and Limits:
    * Note: Elastic Load Balancing logs requests sent to the load balancer, including requests that never made it to the back-end instances
​
    * Limits: Elastic Load Balancing logs requests on a best-effort basis. We recommend that you use access logs to understand the nature of the requests, not as a complete accounting of all requests.
* Log record/file format:
    * Each log entry contains the details of a single request made to the load balancer. All fields in the log entry are delimited by spaces.
    * Format:
        1. timestamp
        2. elb client:port
        3. backend:port
        4. request_processing_time
        5.  backend_processing_time
        6. response_processing_time
        7. elb_status_code
        8. backend_status_code
        9. received_bytes
        10. sent_bytes
        11. "request"
        12. "user_agent"
        13. ssl_cipher
        14. ssl_protocol
* Delivery latency:
    * User defined publishing interval
    (5 min-60 min)
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * S3 bucket
* Encryption at rest:
    * * S3 - AES256, S3 SSE with amazon keys
* Data residency(AWS Region):
    * As per S3 bucket location
* Retention capabilities:
    * S3 -indefinite time/user defined

## Network Load Balancer(NLB) Logs	
* Log coverage:
    * Access logs that capture detailed information about the TLS requests sent to your Network Load Balancer.
    * https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-access-logs.html

* Exceptions and Limits:
    * Access logs are created only if the load balancer has a TLS listener and they contain information only about TLS requests.
* Log record/file format:
    * All fields are delimited by spaces. When new fields are introduced, they are added to the end of the log entry.
* Delivery latency:
    * each 5 min
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * S3 bucket
* Encryption at rest:
    * * S3 - AES256, S3 SSE with amazon keys
* Data residency(AWS Region):
    * As per S3 bucket location
* Retention capabilities:
    * S3 -indefinite time/user defined

## Application Load Balancer(ALB) logs	
* Log coverage:
    * Access Log capture detailed information about requests sent to your load balancer. Each log contains information such as the time the request was received, the client's IP address, latencies, request paths, and server responses
    * https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html
* Exceptions and Limits:
    * Note: Elastic Load Balancing does not log health check requests
    * Limits: Elastic Load Balancing logs requests on a best-effort basis. We recommend that you use access logs to understand the nature of the requests, not as a complete accounting of all requests.
* Log record/file format:
    * Each log entry contains the details of a single request (or connection in the case of WebSockets) made to the load balancer. For WebSockets, an entry is written only after the connection is closed. If the upgraded connection can't be established, the entry is the same as for an HTTP or HTTPS request.
    All fields are delimited by spaces. When new fields are introduced, they are added to the end of the log entry.
* Delivery latency:
    * each 5 min
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * S3 bucket
* Encryption at rest:
    * * S3 - AES256, S3 SSE with amazon keys
* Data residency(AWS Region):
    * As per S3 bucket location
* Retention capabilities:
    * S3 -indefinite time/user defined

## Route53 DNS request
* Log coverage:
    * log information about the queries that Route 53 receives.
The domain or subdomain that was requested
The date and time of the request
The DNS record type (such as A or AAAA)
The Route 53 edge location that responded to the DNS query
The DNS response code, such as NoError or ServFail
* Exceptions and Limits:
    * Query logging is available only for public hosted zones
    * cached response will not be logged

* Log record/file format:
    * newline-delimited log records, Each log record represents one request and consists of space-delimited fields
    * https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/query-logs.html#query-logs-format
    * Fields:
        1. Log format version
        2. Query timestamp
        3. Hosted zone ID
        4. Query name
        5. Query type
        6. Response code
        7. Layer 4 protocol
        8. Route 53 edge location
        9. Resolver IP address
        10. EDNS client subnet
* Delivery latency:
    * N/A
* Transport/Encryption in transit:
* Supported log Destinations:
    * CloudWatch Logs
* Encryption at rest:
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
    * US East (N. Virginia) Region
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined

## Lambda
* Log coverage:
    * Lambda logs all requests handled by your function and also automatically stores logs generated by your code through Amazon CloudWatch Logs
    * https://docs.aws.amazon.com/lambda/latest/dg/monitoring-functions-logs.html
    * You can insert logging statements into your code to help you validate that your code is working as expected. Lambda automatically integrates with CloudWatch Logs and pushes all logs from your code to a CloudWatch Logs group associated with a Lambda function
* Exceptions and Limits:
* Log record/file format:
    JSON?
* Delivery latency:
    * as per CloudWatchLogs
* Transport/Encryption in transit:
    * as per CloudWatchLogs
* Supported log Destinations:
    * CloudWatchLogs
* Encryption at rest:
    * as per CloudWatchLogs
* Data residency(AWS Region):
    * any region
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined

## CloudFront Access Logs
* Log coverage:
    * Logs every user request that CloudFront receives. These access logs are available for both web and RTMP distributions
    * https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html
* Exceptions and Limits:
    * Note, however, that some or all log file entries for a time period can sometimes be delayed by up to 24 hours
* Log record/file format:
    * Web Distribution Log File Format
RTMP Distribution Log File Format
Each entry in a log file gives details about a single user request. The log files for web and for RTMP distributions are not identical, but they share the following characteristics:
Use the W3C extended log file format. (For more information, go to http://www.w3.org/TR/WD-logfile.html.)
Contain tab-separated values.
Contain records that are not necessarily in chronological order.
Contain two header lines: one with the file-format version, and another that lists the W3C fields included in each record.
Substitute URL-encoded equivalents for spaces and non-standard characters in field values.
* Delivery latency:
    * up to several times an hour 
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * S3 bucket
* Encryption at rest:
    * * S3 - AES256, S3 SSE with amazon keys
* Data residency(AWS Region):
    * As per S3 bucket location
* Retention capabilities:
    * S3 -indefinite time/user defined

## Amazon Redshift Logs
* Log coverage:
    * Amazon Redshift logs information about connections and user activities in your database.
    * https://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html
* Exceptions and Limits:
* Log record/file format:
    * Amazon Redshift logs information in the following log files:
        1. Connection log — logs authentication attempts, and connections and disconnections.
        2. User log — logs information about changes to database user definitions.
        3. User activity log — logs each query before it is run on the database.
​
    * Logs format for each of the logs files can be found here: https://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html#db-auditing-logs
* Delivery latency:
    * depends on the Redshift cluster load. More load - more often you get logs
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * S3 bucket
* Encryption at rest:
    * * S3 - AES256, S3 SSE with amazon keys
* Data residency(AWS Region):
    * As per S3 bucket location
* Retention capabilities:
    * S3 -indefinite time/user defined

## Amazon RDS Database Log
* Log coverage:
    * Amazon RDS Database Logs are specific to the database engine:
    * https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.html
* Exceptions and Limits:
* Log record/file format:
    * DataBase engine specific:
        1. MariaDB Database Log Files
        2. Microsoft SQL Server Database Log Files
        3. MySQL Database Log Files
        4. Oracle Database Log Files
        5. PostgreSQL Database Log Files
* Delivery latency:
    * DB engine specific
* Transport/Encryption in transit:
* Supported log Destinations:
    * On DB servers itself
    * CloudWatchLogs
* Encryption at rest:
    * As per DB instance encryption - AES-256 encryption
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
* Retention capabilities:
    * DB-stored logs retention depends on the Db engine (3-7 days)
    * CloudWatch logs: indefinite time/user defined

## Kinesis Data Firehose
* Log coverage:
    * Kinesis Data Firehose integrates with Amazon CloudWatch Logs so that you can view the specific error logs when the Lambda invocation for data transformation or data delivery fails
    * https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-logs.html
* Exceptions and Limits:
* Log record/file format:
    * two log streams named S3Delivery and RedshiftDelivery: S3Delivery log stream is used for logging errors related to delivery failure to the intermediate S3 bucket. The RedshiftDelivery log stream is used for logging errors related to Lambda invocation failure and delivery failure to your Amazon Redshift cluster.
    * Data Delivery Errors:
        1. Amazon S3 Data Delivery Errors
        2. Amazon Redshift Data Delivery Errors
        3. Splunk Data Delivery Errors
        4. Amazon Elasticsearch Service Data Delivery Errors
        5. Lambda Invocation Errors
* Delivery latency:
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
* Encryption at rest:
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined

## Amazon ECS (AWS Fargate)
* Log coverage:
    * You can configure the containers in your tasks to send log information to CloudWatch Logs. This allows you to view the logs from the containers in your Fargate tasks.
    * https://docs.aws.amazon.com/AmazonECS/latest/userguide/using_awslogs.html
* Exceptions and Limits:
    * The type of information that is logged by your task's containers depends mostly on their ENTRYPOINT command. By default, the logs that are captured show the command output that you would normally see in an interactive terminal if you ran the container locally, which are the STDOUT and STDERR I/O streams.
* Log record/file format:
    * STDOUT and STDERR I/O streams
* Delivery latency:
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
* Encryption at rest:
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined

## AWS WAF	
* Log coverage:
    * You can enable logging to get detailed information about traffic that is analyzed by your web ACL. Information that is contained in the logs include the time that AWS WAF received the request from your AWS resource, detailed information about the request, and the action for the rule that each request matched.
    * https://docs.aws.amazon.com/waf/latest/developerguide/logging.html
* Exceptions and Limits:
* Log record/file format:
    * json
    * One AWS WAF log is equivalent to one Kinesis Data Firehose record.
* Delivery latency:
    * near real time
* Transport/Encryption in transit:
* Supported log Destinations:
    * Amazon Kinesis Data Firehose
* Encryption at rest:
    * as for Amazon Kinesis Data Firehose
* Data residency(AWS Region):
    * as for Amazon Kinesis Data Firehose
* Retention capabilities:
    * as for Amazon Kinesis Data Firehose

## API Gateway
* Log coverage:
    * Logs API requests and responses
    * https://docs.aws.amazon.com/apigateway/latest/developerguide/view-cloudwatch-log-events-in-cloudwatch-console.html
* Exceptions and Limits:
    * Note: API Gateway creates log groups or log streams for an API stage at the time when it is deployed
* Log record/file format:
* Delivery latency:
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
* Encryption at rest:
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined

## AWS Systems Manager
* Log coverage:
    * AWS Systems Manager Agent is Amazon software that runs on your Amazon EC2 instances and your hybrid instances that are configured for Systems Manager (hybrid instances).
    you can configure SSM Agent to send log data to Amazon CloudWatch Logs
    * https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-ssm-agent.html
* Exceptions and Limits:
    * Note: The unified CloudWatch Agent has replaced SSM Agent as the tool for sending log data to Amazon CloudWatch Logs
* Log record/file format:
    * system specific logs
* Delivery latency:
    * s per agent settings
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
* Encryption at rest:
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined

## Amazon EMR
* Log coverage:
    * Amazon EMR and Hadoop both produce log files that report status on the cluster.
    There are many types of logs written to the master node. Amazon EMR writes step, bootstrap action, and instance state logs. Apache Hadoop writes logs to report the processing of jobs, tasks, and task attempts. Hadoop also records logs of its daemons.
    * https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-manage-view-web-log-files.html
* Exceptions and Limits:
    * By default, Amazon EMR clusters launched using the console automatically archive log files to Amazon S3. You can specify your own log path, or you can allow the console to automatically generate a log path for you. For clusters launched using the CLI or API, you must configure Amazon S3 log archiving manually.
* Log record/file format:
    * Apache Hadoop specific logs
    * http://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html
    * Amazon EMR writes step, bootstrap action, and instance state logs
* Delivery latency:
    * as logs created
* Transport/Encryption in transit:
    * local to host
* Supported log Destinations:
    * Master node
    * S3
* Encryption at rest:
    * EMR encryption:
    https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-data-encryption-options.html
    * AES256 Encryption: Amazon S3 server-side encryption (SSE)
* Data residency(AWS Region):
    * As per node location
    * As per S3 bucket location
* Retention capabilities:
    * Instance lifetime
    * S3: indefinite time/user defined

## Elastic Beanstalk
* Log coverage:
    * The Amazon EC2 instances in your Elastic Beanstalk environment generate logs that you can view to troubleshoot issues with your application or configuration files. Logs created by the web server, application server, Elastic Beanstalk platform scripts, and AWS CloudFormation are stored locally on individual instances
    * https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html
* Exceptions and Limits:
* Log record/file format:
    * These logs contain messages about deployment activities, including messages related to configuration files (.ebextensions).
    * Linux
        * /var/log/eb-activity.log
        * /var/log/eb-commandprocessor.log
        * /var/log/eb-version-deployment.log
    * Windows Server
        * C:\Program Files\Amazon\ElasticBeanstalk\logs\
        * C:\cfn\logs\cfn-init.log
    * Each application and web server stores logs in its own folder:
        * Apache – /var/log/httpd/
        * IIS – C:\inetpub\wwwroot\
        * Node.js – /var/log/nodejs/
        * nginx – /var/log/nginx/
        * Passenger – /var/app/support/logs/
        * Puma – /var/log/puma/
        * Python – /opt/python/log/
        * Tomcat – /var/log/tomcat8/
* Delivery latency:
    * as logs created - near real time
* Transport/Encryption in transit:
    * locally on the instance
    * logrotate to S3
* Supported log Destinations:
    * instance
    * CloudWatch Logs
    * S3
* Encryption at rest:
    * Instance encryption
    * As per CloudWatchLogs configuration (see below)
    * AES256 Encryption: Amazon S3 server-side encryption (SSE)
* Data residency(AWS Region):
    * As per instance location
    * any region
    * As per S3 bucket location
* Retention capabilities:
    * Instance lifetime
    * CloudWatch logs: indefinite time/user defined
    * Elastic Beanstalk deletes tail and bundle logs from Amazon S3 automatically 15 minutes after they are created. Rotated logs persist.

## OpsWorks
* Log coverage:
    * To simplify the process of monitoring logs on multiple instances, AWS OpsWorks Stacks supports Amazon CloudWatch Logs
    * https://docs.aws.amazon.com/opsworks/latest/userguide/monitoring-cloudwatch-logs.html
* Exceptions and Limits:
* Log record/file format:
    * OS/app specifi
* Delivery latency:
    * as per  AWS OpsWorks Stacks agent
* Transport/Encryption in transit:
    * internal to AWS, hopefully https
* Supported log Destinations:
    * CloudWatch Logs
* Encryption at rest:
    * As per CloudWatchLogs configuration
* Data residency(AWS Region):
* Retention capabilities:
    * CloudWatch logs: indefinite time/user defined


# AWS Built-in Centralized logging capabilities
## <a name="cloudwatchlogs"></a> Amazon CloudWatch Logs Service

Amazon CloudWatch Logs could be used to monitor, store, and access your log files from Amazon Elastic Compute Cloud (Amazon EC2) instances, AWS CloudTrail, Route 53, and other sources. You can then retrieve the associated log data from CloudWatch Logs.
https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html

**Service coverage:**

* Logs from Amazon EC2 Instances
    * *Logs Retrieval:* AWS provide agent (several different version are available)
    * *Delivery schedule:* as per agent settings
    * *Data residency:* any region
* Route 53 DNS Queries
    * *Logs Retrieval:* Service push
    * *Delivery schedule:*
    * *Data residency:* 	US East (N. Virginia) Region only
* VPC Flow Logs:
    * *Logs Retrieval:* Service push: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-cwl.html
    * *Delivery schedule:* 
    * *Data residency:* 
* Lambda function Logs
    * *Logs Retrieval:* Service push
    * *Delivery schedule:* 
    * *Data residency:* any aws region
* Amazon RDS Database Log
    * *Logs Retrieval:* Service push
    * *Delivery schedule:* as per DB engine configuration
    * *Data residency:* any aws region
* Kinesis Data Firehose
    * *Logs Retrieval:* Service push
    * *Delivery schedule:* 
    * *Data residency:* any aws region
* Amazon ECS (AWS Fargate)
    * *Logs Retrieval:* Service push
    * *Delivery schedule:* 
    * *Data residency:* any aws region
* API Gateway
    * *Logs Retrieval:* Service push
    * *Delivery schedule:* 
    * *Data residency:* any aws region
* AWS Systems Manager
    * *Logs Retrieval:* Agent push
    * *Delivery schedule:* as per agent configuration
    * *Data residency:* any aws region
* Elastic Beanstalk
    * *Logs Retrieval:* Agent push
    * *Delivery schedule:* as per agent/service configuration
    * *Data residency:* any aws region
* OpsWorks
    * *Logs Retrieval:* OpsWorks Stacks agent push
    * *Delivery schedule:* as per agent configuration
    * *Data residency:* any aws region
* AWS Global Accelerator flow logs
    * *Logs Retrieval:* Service push through s3 : https://docs.aws.amazon.com/global-accelerator/latest/dg/monitoring-global-accelerator.flow-logs.html#monitoring-global-accelerator.flow-logs-publishing-S3
    * *Delivery schedule:* as per agent configuration
    * *Data residency:* any aws region

**Encryption at REST:**

AWS Key Management Service (AWS KMS) key: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html

**Retention policy:**

CloudWatch logs: logs are kept indefinitely and never expire. User can create retention policy per log group with following option: indefinite, or from 1 day to 10years 
Data visualization and analyzes:
CloudWatch Logs Insights: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html
Metric filters: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html

**Notification and alerting:**

CloudWatch Alarms: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html

**Real time processing options:**
Real-time Processing of Log Data with Subscriptions: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions.html
Supported AWS Services for the real time data processing: AWS Kinesis, Lambda

**Data export and external tool integrations:**
    * Export data to S3: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3Export.html
    * Streaming data to the Amazon Elasticsearch Service: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_ES_Stream.html
**Known limits:**

Amazon CloudWatch Logs limits: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/cloudwatch_limits_cwl.html

**AWS recommended solutions/implementations**:

https://aws.amazon.com/answers/logging/centralized-logging/
​






# Templates

## Serice Template:
* Log coverage:
* Exceptions and Limits:
* Log record/file format:
* Delivery latency:
* Transport/Encryption in transit:
* Supported log Destinations:
* Encryption at rest:
* Data residency(AWS Region):
* Retention capabilities:

## Cloudwatchlogs service template
* *Logs Retrieval:*
* *Delivery schedule:*
* *Data residency:*