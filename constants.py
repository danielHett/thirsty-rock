# Policy stuff...
EC2_POLICY_NAME = 'thirsty-rock-ec2-policy'
EC2_POLICY_DESCRIPTION = 'A policy used for the role used by the thirsty-rock EC2 servers'
EC2_POLICY_DOCUMENT = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RandomPermission",
            "Effect": "Allow",
			"Action": [
				"iam:ListPolicies"
			],
            "Resource": "*",
        }
    ]
} 

# Role stuff...
EC2_ROLE_NAME = 'thirsty-rock-ec2-role'
EC2_ROLE_DESCRIPTION = 'The role used by the thirsty-rock EC2 servers'
EC2_ASSUME_ROLE_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
} 

# Security group stuff...
EC2_SECURITY_GROUP_NAME = 'thirsty-rock-security-group'

# Instance profile stuff... (why does this even exist?). 
EC2_INSTANCE_PROFILE_NAME = 'thirsty-rock-ec2-instance-profile'