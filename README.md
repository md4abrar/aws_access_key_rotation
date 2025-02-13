# AWS Access Key Rotation

**Automated solution for rotating AWS IAM Access Keys and updating them in AWS Secrets Manager.**

## Overview

Managing AWS IAM Access Keys securely is crucial for maintaining the integrity and security of your AWS environment. This project provides an automated approach to rotate AWS IAM Access Keys and update the corresponding credentials in AWS Secrets Manager, ensuring that your applications always use the most recent and secure access keys.

## Features

- **Automated Key Rotation**: Utilizes AWS Lambda to automatically rotate IAM Access Keys.
- **Secrets Manager Integration**: Updates the rotated keys in AWS Secrets Manager for seamless access by applications.
- **CloudFormation Deployment**: Provides an AWS CloudFormation template for easy deployment and setup.

## Prerequisites

Before deploying this solution, ensure you have the following:

- **AWS Account**: Active AWS account with necessary permissions.
- **AWS CLI**: Installed and configured on your local machine.
- **AWS CloudFormation**: Permissions to deploy stacks and create IAM roles and policies.

## Deployment Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/md4abrar/aws_access_key_rotation.git
cd aws_access_key_rotation
```

### 2. Deploy CloudFormation Stack

Use the provided CloudFormation template to set up the necessary AWS resources:

```bash
aws cloudformation deploy \
    --template-file iam-key-auto-rotation-iam-assumed-roles.yaml \
    --stack-name aws-access-key-rotation-stack \
    --capabilities CAPABILITY_NAMED_IAM
```

*Note*: Ensure that the IAM roles and policies defined in the template align with your organization's security policies.

### 3. Update Trust Policy

If you encounter issues during stack creation, such as:

```
Role [role_arn] is invalid or cannot be assumed.
```

Update the trust policy of the role you're using to create the stack:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudformation.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### 4. Configure Lambda Function

The `rotate-secret-and-update-aws-sm.py` script contains the AWS Lambda function code responsible for rotating the access keys and updating AWS Secrets Manager. Deploy this function and set up the necessary triggers as per your requirements.

## Project Structure

```
aws_access_key_rotation/
├── iam-key-auto-rotation-iam-assumed-roles.yaml
├── rotate-secret-and-update-aws-sm.py
├── LICENSE
└── README.md
```

- `iam-key-auto-rotation-iam-assumed-roles.yaml`: CloudFormation template for setting up IAM roles and policies.
- `rotate-secret-and-update-aws-sm.py`: Lambda function script for rotating access keys and updating Secrets Manager.
- `LICENSE`: Project license information.
- `README.md`: Project documentation.


### Troubleshooting:

If you get any issues while creating the cloudformation stack like "Role [role_arn] is invalid or cannot be assumed”". Please update the trust policy of the role that you are using to create the stack

  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "cloudformation.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }


## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](https://github.com/md4abrar/aws_access_key_rotation/blob/master/LICENSE) file for details.
