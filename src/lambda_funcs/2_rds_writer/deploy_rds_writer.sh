aws s3api create-bucket \
--bucket lawn-rds-writer-src \
--region us-east-1

sam deploy \
--stack-name lawnRDSwriter \
--s3-bucket lawn-rds-writer-src \
--capabilities CAPABILITY_IAM