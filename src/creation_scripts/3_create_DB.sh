aws cloudformation create-stack \
--stack-name lawnDB \
--template-body file://../CF_templates/3_lawnDB.yml \
--on-failure DELETE \