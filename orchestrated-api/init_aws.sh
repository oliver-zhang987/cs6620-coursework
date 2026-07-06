#!/bin/bash
# Runs inside LocalStack after services are ready.
# Creates the DynamoDB table and S3 bucket that the API needs.

awslocal dynamodb create-table \
    --table-name items \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

awslocal s3 mb s3://items-bucket

echo "init_aws.sh: DynamoDB table 'items' and S3 bucket 'items-bucket' created."
