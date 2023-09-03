import boto3
import os

instance_id = os.environ['INSTANCE_ID']
ssm_parameter = os.environ['SSM_PARAMETER']
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

# stop instance
# create snapshot of ebs volume
# wait until its done
# detach volume from instance
# delete volume