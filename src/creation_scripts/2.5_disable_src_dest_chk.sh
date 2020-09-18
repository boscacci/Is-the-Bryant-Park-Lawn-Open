#!/bin/bash
aws ec2 modify-instance-attribute \
--source-dest-check "{\"Value\": false}" \
--instance-id ${NAT_ID}