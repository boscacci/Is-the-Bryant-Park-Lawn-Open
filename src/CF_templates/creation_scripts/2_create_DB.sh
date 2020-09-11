aws cloudformation create-stack \
--stack-name lawnDB \
--template-body file://../2_lawnDB.yml \
--on-failure DELETE