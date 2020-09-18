aws cloudformation create-stack \
--stack-name lawnSecurity \
--template-body file://../CF_templates/1_lawnSecurity.yml \
--capabilities CAPABILITY_NAMED_IAM \
--on-failure DELETE