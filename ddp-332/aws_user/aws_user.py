#!/usr/bin/python
# -*- coding: utf-8 -*-

"""aws_user: Manages k8s-console users.

aws-user automates the process of creating and deleteing temporary users.
- Manage temporary users
  - Creating them
  - Deleteing them
"""


import boto3
import click

from user import UserManager


session = boto3.Session(profile_name='pt-operator')
user_manager = UserManager(session)


@click.group()
def cli():
    """aws-user manages AWS temporary users for firefighter access."""
    pass


@cli.command('list-users')
def list_users():
    """List all k8s-console users."""
    for user in user_manager.all_users():
        print(user)


@cli.command('generate-user')
def generate_user():
    """Generate a k8s-console user."""
    user_manager.generate_user()
    print('UserName = {}\nAccessKeyId = {}\nSecretAccessKey = {}'
          .format(
              user_manager.user_name,
              user_manager.access_key,
              user_manager.secret_key
          ))


@cli.command('delete-user')
@click.argument('username')
@click.argument('accesskeyid')
def delete_user(username, accesskeyid):
    """Delete a given k8s-console user."""
    user_manager.delete_user(username, accesskeyid)


if __name__ == '__main__':
    cli()
