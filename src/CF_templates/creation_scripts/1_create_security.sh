aws cloudformation create-stack \
--stack-name lawnSecurity \
--template-body file://../1_lawnSecurity.yml \
--on-failure DELETE