aws s3api create-bucket \
--bucket lawn-viz-gen-src \
--region us-east-1

sam deploy \
--stack-name lawnVizGen \
--s3-bucket lawn-viz-gen-src \
--capabilities CAPABILITY_IAM