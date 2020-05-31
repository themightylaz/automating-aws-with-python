#!/usr/bin/python
# -*- coding: utf-8 -*-

"""aws_user: Manages k8s-console users.

aws-user automates the process of creating and deleteing temporary users.
- Manage temporary users
  - Creating them
  - Deleteing them
"""

import string
import random

import boto3
from botocore.exceptions import ClientError
import click


session = boto3.Session(profile_name='pt-operator')

iam_client = session.client('iam')

tags = [{'Key': 'CostCenter', 'Value': 'D2'},
        {'Key': 'Service', 'Value': 'k8s-console'},
        {'Key': 'Team', 'Value': 'DPML'},
        {'Key': 'Department', 'Value': 'Data'},
        {'Key': 'Jira', 'Value': 'DDP-332'},
        {'Key': 'Environment', 'Value': 'PT'}]


def generate_username(size=10, chars=string.ascii_lowercase + string.digits):
    """Generate a user name with random suffix."""
    suffix = ''.join(random.choice(chars) for _ in range(size))
    return 'k8s-console-temp-user-' + suffix


@click.group()
def cli():
    """aws-user manages AWS temporary users for firefighter access."""
    pass


@cli.command('list-users')
def list_users():
    """List all k8s-console users."""
    user_list = iam_client.list_users(MaxItems=100)
    for user in user_list['Users']:
        filter_dict = {k: v for (k, v) in user.items() if 'UserName' in k}
        filter_value = filter_dict.get('UserName')
        if filter_value.startswith('k8s-console-temp-user-'):
            print(filter_value)


def create_access_key(username):
    """Create access key pair for given user."""
    return iam_client.create_access_key(UserName=username)


def delete_access_key(username, accesskeyid):
    """Delete access key pair for given user."""
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=accesskeyid)
    except ClientError as error:
        if error.response['Error']['Code'] == 'NoSuchEntityException':
            pass
        else:
            raise


@cli.command('generate-user')
def generate_user():
    """Generate a k8s-console user."""
    user = iam_client.create_user(UserName=generate_username(), Tags=tags)
    username = user['User']['UserName']
    accesskey = create_access_key(username)
    print('UserName = {}\nAccessKeyId = {}\nSecretAccessKey = {}'
          .format(
              username,
              accesskey['AccessKey']['AccessKeyId'],
              accesskey['AccessKey']['SecretAccessKey']
          ))


@cli.command('delete-user')
@click.argument('username')
@click.argument('accesskeyid')
def delete_user(username, accesskeyid):
    """Delete a given k8s-console user."""
    delete_access_key(username, accesskeyid)
    iam_client.delete_user(UserName=username)


if __name__ == '__main__':
    cli()
