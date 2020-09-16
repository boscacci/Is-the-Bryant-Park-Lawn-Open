aws s3api create-bucket \
--bucket lawn-scraper-src \
--region us-east-1

sam deploy \
--stack-name lawnFuncs \
--s3-bucket lawn-scraper-src \
--capabilities CAPABILITY_IAM