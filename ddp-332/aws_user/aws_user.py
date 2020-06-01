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

from aws_user.user import UserManager

session = None
user_manager = None


@click.group()
@click.option('--profile', default=None, help="Use a given AWS profile.")
def cli(profile):
    """aws-user manages AWS temporary users for firefighter access."""
    global session, user_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    user_manager = UserManager(session)


@cli.command('list-users')
def list_users():
    """List all k8s-console users."""
    for user in user_manager.all_users():
        print(user)


@cli.command('generate-user')
def generate_user():
    """Generate a k8s-console user."""
    user_manager.generate_user()
    user_manager.print_userdata()


# @cli.command('delete-user')
# @click.argument('username')
# @click.argument('accesskeyid')
# def delete_user(username, accesskeyid):
#     """Delete a given k8s-console user."""
#     user_manager.delete_user(username, accesskeyid)


# @cli.command('delete-stored-user')
@cli.command('delete-user')
@click.argument('username')
def delete_stored_user(username):
    """Delete a given k8s-console user."""
    user_manager.delete_stored_user(username)


@cli.command('list-user-details')
@click.argument('username')
def list_user_details(username):
    """Delete a given k8s-console user."""
    user_manager.list_user_details(username)


if __name__ == '__main__':
    cli()
