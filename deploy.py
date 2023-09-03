#!/usr/bin/env python3

import argparse
from datetime import datetime

import aws_cdl

parser = argparse.ArgumentParser(description='Tool to deploy ec2-ebs-cost-saving')
parser.add_argument('-p', '--profile', required=True, help='AWS CLI profile to use for the deplyoment')
parser.add_argument('-r', '--region', required=True, help='AWS Region to deploy this solution into')
parser.add_argument('-i', '--instanceid', required=True, help='Instance ID for which this solution should be used for')
parser.add_argument('-t', '--template', default='cfn_template.yaml' , help='Cloudformation Template file to use. Default: cfn_template.yaml')
args = parser.parse_args()
