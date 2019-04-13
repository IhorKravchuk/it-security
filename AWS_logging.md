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



















* Log coverage:
* Exceptions and Limits:
* Log record/file format:
* Delivery latency:
* Transport/Encryption in transit:
* Supported log Destinations:
* Encryption at rest:
* Data residency(AWS Region):
* Retention capabilities: