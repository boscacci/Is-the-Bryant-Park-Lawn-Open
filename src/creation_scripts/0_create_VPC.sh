aws cloudformation create-stack \
--stack-name lawnVPC \
--template-body file://../CF_templates/0_lawnVPC.yml \
--on-failure DELETE