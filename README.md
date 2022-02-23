# aws_access_key_rotation

Troubleshooting:

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
