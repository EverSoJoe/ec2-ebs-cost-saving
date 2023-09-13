#!/usr/bin/env python3

import argparse
from datetime import datetime

import aws_cdl

parser = argparse.ArgumentParser(description='Tool to deploy ec2-ebs-cost-saving')
parser.add_argument('-p', '--profile', required=True, help='AWS CLI profile to use for the deplyoment')
parser.add_argument('-r', '--region', required=True, help='AWS Region to deploy this solution into')
parser.add_argument('-i', '--instanceid', required=True, help='Instance ID for which this solution should be used for')
parser.add_argument('-m', '--mountpoint', required=True, help='Mount point to mount Volume after restore')
parser.add_argument('-t', '--template', default='cfn_template.yaml' , help='Cloudformation Template file to use. Default: cfn_template.yaml')
parser.add_argument('-b', '--bucket', help='Bucket to upload the code to. Will be created if not existing. Files will be deleted from bucket after deployment. Defaults to <account-alias>-lambda-code')
parser.add_argument('-d', '--delete', action='store_true', help='If set, will delete the ressources that control the given instance')
parser.add_argument('-f', '--force', action='store_true', help='If set, will delete the stack before deployment. Necessary if previous deployment failed')
args = parser.parse_args()

stack_name = 'start-stop-%s' %(args.instanceid)
lambda_start_key = 'start-instance-%s' %(datetime.now().isoformat())
lambda_stop_key = 'stop-instance-%s' %(datetime.now().isoformat())
if not args.bucket:
    account_alias = boto3.Session(profile_name=args.profile, region_name = args.region).client('iam').list_account_aliases()['AccountAliases'][0]
    setattr(args, 'bucket', '%s-lambda-code' %(account_alias))
cfn_parameters = [
    {'ParameterKey': 'InstanceId',
     'ParameterValue': args.instanceid},
    {'ParameterKey': 'MountPoint',
     'ParameterValue': args.mountpoint},
    {'ParameterKey': 'LambdaCodeBucket',
     'ParameterValue': args.bucket},
    {'ParameterKey': 'LambdaStartCodeKey',
     'ParameterValue': lambda_start_key},
    {'ParameterKey': 'LambdaStopCodeKey',
     'ParameterValue': lambda_stop_key}
]
cfn_client = aws_cdl.create_cf_client(args.profile, args.region)

if delete_stack:
    aws_cdl.delete_stack(cfn_client, stack_name)
else:
    aws_cdl.upload_lambda_package(args.profile, 'start-instance-lambda', args.bucket, lambda_start_key, args.region)
    aws_cdl.upload_lambda_package(args.profile, 'stop-instance-lambda', args.bucket, lambda_stop_key, args.region)
    try:
        aws_cdl.create_update_stack(cfn_client, args.template, cfn_parameter, stack_name, args.force)
    except Exception as e:
        print(e)
    finally:
        aws_cdl.delete_lambda_package(args.profile, args.bucket, lambda_start_key, args.region)
        aws_cdl.delete_lambda_package(args.profile, args.bucket, lambda_stop_key, args.region)

