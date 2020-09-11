aws cloudformation create-stack \
--stack-name lawnVPC \
--template-body file://../0_lawnVPC.yml \
--on-failure DELETE