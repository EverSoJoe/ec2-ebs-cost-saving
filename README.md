# AWS EC2 EBS Cost Savings
This project contains two AWS Lambda Functions written in Python to start and stop an instance while trying to minimize cost while the machine is stopped by creating an EBS Snapshot and deleting the EBS Volume.

This assumes you are already using an EC2 Instance that you want to save cost on due to it not running 24/7

## Stopping an instance
When stopping an instance, a Lambda Function will first stop the EC2 Instance, then create an EBS Snapshot of the EBS Volume attached to the EC2 Instance. After that is done, it will detach and delete the EBS Volume.

## Starting an instance
When starting an instance, a Lambda Function will first restore a EBS Snapshot and attach the resulting EBS Volume to the required mounting point of an EC2 Instance before starting that instance

## AWS Services used
- Cloudfomration (For deployment)
- Lambda (For the actual starting and stopping)
- SSM (For storing the EBS Snapshot ID)

## Deployment
´deploy.py -h´