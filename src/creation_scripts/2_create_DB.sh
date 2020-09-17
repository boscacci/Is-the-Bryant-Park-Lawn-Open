aws cloudformation create-stack \
--stack-name lawnDB \
--template-body file://../CF_templates/2_lawnDB.yml \
--on-failure DELETE \
--stack-policy-body file://../CF_templates/2_DB_stackPolicy.json