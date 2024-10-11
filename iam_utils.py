import logging
import boto3
import json
import constants

def setup_ec2_role():
    logging.info('Start setup_ec2_role')

    # First, let's check if there is a policy out there.  
    ec2_iam_policy = get_ec2_iam_policy()

    # If it doesn't exist, make it!
    if (ec2_iam_policy is None):
        logging.info('The policy did not exist')
        ec2_iam_policy = create_ec2_iam_policy()

    # Now we validate that the policy has all of the necessary permissions.  
    # For now, this returns True. TODO: Write the code that validates the permissions. 
    if (not is_valid_ec2_iam_policy(ec2_iam_policy)):
        logging.info('The policy does not have the correct permissions')

    # At this point, we know there is a policy out there which we can use. 
    # Now we check if the role exists. If not, we make a new role with the policy attached.  
    ec2_iam_role = get_ec2_iam_role()
    
    # If it doesn't exist, make it!
    if (ec2_iam_role is None):
        logging.info('The EC2 role did not exist')
        ec2_iam_role = create_ec2_iam_role()

    attach_policy(ec2_iam_role, ec2_iam_policy)

    create_instance_profile()



def get_ec2_iam_role():
    logging.info('Starting get_ec2_iam_role')

    client = boto3.client('iam')

    try:
        roles = client.list_roles()['Roles']
    except:
        raise Exception("Encountered an error while calling out to IAM.")
    
    for role in roles:
        logging.debug(role)
        if role['RoleName'] == constants.EC2_ROLE_NAME:
            logging.info('A role with a matching name was found')
            logging.info(role)
            return role
    
    logging.info('No matching role was found')
    return None

def get_ec2_iam_policy():
    logging.info('Starting get_ec2_iam_policy')

    client = boto3.client('iam')

    try: 
        policies = client.list_policies(
            Scope='Local',
            OnlyAttached=False,
        )['Policies']
    except:
        raise Exception("Encountered an error while calling out to IAM.")
    
    for policy in policies:
        logging.debug(policy)
        if policy['PolicyName'] == constants.EC2_POLICY_NAME:
            logging.info('A policy with a matching name was found')
            logging.info(policy)            
            return policy
        
    logging.info('No matching policy was found')
    return None

def create_ec2_iam_policy():
    logging.info('Starting create_ec2_iam_policy')

    client = boto3.client('iam')

    try:
        policy = client.create_policy(
            PolicyName=constants.EC2_POLICY_NAME,
            PolicyDocument=json.dumps(constants.EC2_POLICY_DOCUMENT),
            Description=constants.EC2_POLICY_DESCRIPTION,
        )['Policy']
    except:
        raise Exception("Encountered an error while calling out to IAM.")
    
    logging.info('The policy that was created: ')
    logging.info(policy)

    return policy

def is_valid_ec2_iam_policy(policy):
    logging.info('Starting is_valid_ec2_iam_policy')

    return True

def create_ec2_iam_role():
    logging.info('Starting create_ec2_iam_role')

    client = boto3.client('iam')

    try:
        role = client.create_role(
            RoleName=constants.EC2_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(constants.EC2_ASSUME_ROLE_POLICY),
            Description=constants.EC2_ROLE_DESCRIPTION
        )['Role']
    except:
        raise Exception("Encountered an error while calling out to IAM.")

    logging.info('The role that was created: ')
    logging.info(role)

    return role

def attach_role_to_profile():
    logging.info('Starting attach_role_to_profile')

    client = boto3.client('iam')

    try: 
        client.add_role_to_instance_profile(
            InstanceProfileName=constants.EC2_INSTANCE_PROFILE_NAME,
            RoleName=constants.EC2_ROLE_NAME
        )

    except Exception:
        raise Exception("Encountered an error while calling out to IAM.")

def attach_policy(role, policy):
    logging.info('Starting attach_policy with (role, policy)')
    logging.info(role)
    logging.info(policy)

    client = boto3.client('iam')

    try:
        client.attach_role_policy(
            RoleName=role['RoleName'],
            PolicyArn=policy['Arn']
        )
    except:
        raise Exception("Encountered an error while calling out to IAM.")

    logging.info('Attach successful')

"""
Creates an instance profile and attaches the role from the constants file. This function expects that the role
has already been created!
"""
def create_instance_profile():
    logging.info('Starting create_instance_profile')

    client = boto3.client('iam')

    profile = None
    try:
        profile = client.get_instance_profile(InstanceProfileName=constants.EC2_INSTANCE_PROFILE_NAME)['InstanceProfile']
    except Exception as error:
        if 'NoSuchEntityException' not in str(error):
            raise Exception("Encountered an error while trying to fetch an instance profile.")

    if profile is None:
        profile = client.create_instance_profile(InstanceProfileName=constants.EC2_INSTANCE_PROFILE_NAME)['InstanceProfile']
    
    roles = profile['Roles']
    if len(roles) > 0:
        client.remove_role_from_instance_profile(
            InstanceProfileName=constants.EC2_INSTANCE_PROFILE_NAME,
            RoleName=roles[0]['RoleName']
        )
    
    client.add_role_to_instance_profile(
            InstanceProfileName=constants.EC2_INSTANCE_PROFILE_NAME,
            RoleName=constants.EC2_ROLE_NAME
    )
    