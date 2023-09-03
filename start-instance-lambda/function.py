import boto3
import os

instance_id = os.environ['INSTANCE_ID']
mount_point = os.environ['MOUNT_POINT']
ssm_parameter = os.environ['SSM_PARAMETER']
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

# read snapshot id from ssm parameter
# restore snapshot
# wait for it to restore
# attach resulting ebs to mount point of instance
# start instance