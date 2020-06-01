# -*- coding: utf-8 -*-

"""Classes for IAM users."""


import string
import random
import shelve

from botocore.exceptions import ClientError
from aws_user.tags import get_tags


class UserManager:
    """Manage k8s-console temporary users."""

    def __init__(self, session):
        """Create a UserManager object."""
        self.session = session
        self.iam_client = self.session.client('iam')
        self.__userdata = {}

    @property
    def userdata(self):
        """Getter function for userdata."""
        return self.__userdata

    @userdata.setter
    def userdata(self, userdata):
        """Setter function for user_name."""
        self.__userdata = userdata

    def all_users(self):
        """Get an iterator for all k8s-console users."""
        user_list = self.iam_client.list_users(MaxItems=100)
        k8s_user_list = []

        for user in user_list['Users']:
            filter_dict = {k: v for (k, v) in user.items() if 'UserName' in k}
            filter_value = filter_dict.get('UserName')
            if filter_value.startswith('k8s-console-temp-user-'):
                k8s_user_list.append(filter_value)

        return k8s_user_list

    def create_access_key(self, username):
        """Create access key pair for given user."""
        return self.iam_client.create_access_key(UserName=username)

    def delete_access_key(self, username, accesskeyid):
        """Delete access key pair for given user."""
        try:
            self.iam_client.delete_access_key(
                UserName=username,
                AccessKeyId=accesskeyid
            )
        except ClientError as error:
            if error.response['Error']['Code'] == 'NoSuchEntityException':
                pass
            else:
                raise

    @staticmethod
    def generate_username(size=10, chars=string.ascii_lowercase + string.digits):
        """Generate a user name with random suffix."""
        suffix = ''.join(random.choice(chars) for _ in range(size))
        return 'k8s-console-temp-user-' + suffix

    def generate_user(self):
        """Generate a k8s-console user."""
        user = self.iam_client.create_user(
            UserName=self.generate_username(),
            Tags=get_tags()
        )
        username = user['User']['UserName']
        accesskey = self.create_access_key(username)

        self.userdata = {
            'UserName': username,
            'AccessKey': accesskey['AccessKey']['AccessKeyId'],
            'SecretKey': accesskey['AccessKey']['SecretAccessKey']
        }

        with shelve.open('userdata.db') as db:
            userdata_without_secret = self.userdata
            userdata_without_secret['SecretKey'] = '<hidden>'
            db[username] = userdata_without_secret

    def print_userdata(self):
        """Print out details for generated user."""
        print('UserName = {}\nAccessKeyId = {}\nSecretAccessKey = {}'
              .format(
                  self.userdata['UserName'],
                  self.userdata['AccessKey'],
                  self.userdata['SecretKey']
              ))

    def list_user_details(self, username):
        """Print out details for an existing user."""
        with shelve.open('userdata.db') as db:
            self.userdata = db[username]
        self.print_userdata()

    def delete_user(self, username, accesskeyid):
        """Delete a given k8s-console user."""
        self.delete_access_key(username, accesskeyid)
        self.iam_client.delete_user(UserName=username)

    def delete_stored_user(self, username):
        """Delete a given k8s-console user."""
        with shelve.open('userdata.db') as db:
            self.userdata = db[username]

        if username == self.userdata['UserName']:
            self.delete_access_key(username, self.userdata['AccessKey'])
            self.iam_client.delete_user(UserName=username)
        else:
            print('Warning: User {} does not exist.'.format(username))
