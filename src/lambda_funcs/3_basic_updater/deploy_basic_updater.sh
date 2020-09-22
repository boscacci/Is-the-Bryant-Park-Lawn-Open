aws s3api create-bucket \
--bucket lawn-status-updater-src \
--region us-east-1

sam deploy \
--stack-name lawnBasicUpdater \
--s3-bucket lawn-status-updater-src \
--capabilities CAPABILITY_IAM