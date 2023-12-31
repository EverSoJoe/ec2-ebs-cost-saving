import boto3
import os

instance_id = os.environ['INSTANCE_ID']
ssm_parameter = os.environ['SSM_PARAMETER']
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def handler(event, context):
    ec2.stop_instances(InstanceIds=[instance_id])
    stopped = False
    while not stopped:
        response = ec2.describe_instances(
            InstanceIds=[instance_id]
        )
        if response['Reservations'][0]['Instances'][0]['State']['Name'] == 'stopped':
            stopped = True
    volume_id = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    response = ec2.create_snapshot(
        VolumeId=volume_id
    )
    snapshot_id = response['SnapshotId']
    ssm.put_parameter(
        Name=ssm_parameter,
        Value=snapshot_id,
        Overwrite=True
    )
    response = ec2.detach_volume(
        VolumeId=volume_id
    )
    while response['State'] != 'detached':
        try:
            response = ec2.detach_volume(
                VolumeId=volume_id
            )
        except ec2.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'IncorrectState':
                break
    ec2.delete_volume(
        VolumeId=volume_id
    )