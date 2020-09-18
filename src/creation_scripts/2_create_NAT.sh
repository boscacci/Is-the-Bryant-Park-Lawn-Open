aws cloudformation create-stack \
--stack-name lawnNAT \
--template-body file://../CF_templates/2_lawnNATinstance.yml \
--on-failure DELETE