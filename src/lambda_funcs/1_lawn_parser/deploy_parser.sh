aws s3api create-bucket \
--bucket lawn-parser-src \
--region us-east-1

sam deploy \
--stack-name lawnFuncs \
--s3-bucket lawn-parser-src \
--capabilities CAPABILITY_IAM