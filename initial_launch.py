"""
This is the script that launches the initial EC2 server.  
"""
import boto3
import constants
import iam_utils

# TODO: Validate that the user has the required permissions on AWS to run this script!

iam_utils.setup_ec2_role()


# the ec2 server needs the correct security group. 


user_data = ""
with open('on_demand_script.sh', 'r') as f:
    user_data = f.read()

client = boto3.client('ec2', region_name='us-east-1')

response = client.run_instances(
    ImageId='ami-0ebfd941bbafe70c6',
    InstanceType='t3a.nano',
    MaxCount=1,
    MinCount=1,
    Monitoring={
        'Enabled': False
    },
    InstanceInitiatedShutdownBehavior='terminate',
    UserData=user_data,
    IamInstanceProfile={
        'Name': constants.EC2_INSTANCE_PROFILE_NAME
    },
    SecurityGroupIds=[
        'sg-04efd2ec993dbc91a',
    ],
    KeyName='connection_key'
)

print(response)
