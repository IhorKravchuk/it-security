# Native AWS logging capabilities
official doc (missing a lot of services): https://aws.amazon.com/answers/logging/aws-native-security-logging-capabilities/

## CloudTrail
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














* Log coverage:
* Exceptions and Limits:
* Log record/file format:
* Delivery latency:
* Transport/Encryption in transit:
* Supported log Destinations:
* Encryption at rest:
* Data residency(AWS Region):
* Retention capabilities: