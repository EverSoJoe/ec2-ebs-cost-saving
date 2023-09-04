import boto3
import os

instance_id = os.environ['INSTANCE_ID']
mount_point = os.environ['MOUNT_POINT']
ssm_parameter = os.environ['SSM_PARAMETER']
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def handler(event, context):
    availability_zone = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
    snapshot_id = ssm.get_parameter(Name=ssm_parameter)['Parameter']['Value']
    response = ec2.create_volume(
        AvailabilityZone=availability_zone,
        SnapshotId=snapshot_id,
        VolumeType='gp3'
    )
    volume_id = response['VolumeId']
    ec2.attach_volume(
        Device=mount_point,
        InstanceId=instance_id,
        VolumeId=volume_id
    )
    ec2.start_instances(InstanceIds=[instance_id])
    ec2.delete_snapshot(SnapshotId=snapshot_id)