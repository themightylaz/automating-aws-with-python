# -*- coding: utf-8 -*-

"""Classes for IAM users."""


import string
import random

from botocore.exceptions import ClientError
from tags import get_tags


class UserManager:
    """Manage k8s-console temporary users."""

    def __init__(self, session):
        """Create a UserManager object."""
        self.session = session
        self.iam_client = self.session.client('iam')
        self.__user_name = ''
        self.__access_key = ''
        self.__secret_key = ''

    @property
    def user_name(self):
        """Getter function for user_name."""
        return self.__user_name

    @property
    def access_key(self):
        """Getter function for access_key."""
        return self.__access_key

    @property
    def secret_key(self):
        """Getter function for secret_key."""
        return self.__secret_key

    @user_name.setter
    def user_name(self, username):
        """Setter function for user_name."""
        self.__user_name = username

    @access_key.setter
    def access_key(self, accesskey):
        """Setter function for access_key."""
        self.__access_key = accesskey

    @secret_key.setter
    def secret_key(self, secretkey):
        """Setter function for secret_key."""
        self.__secret_key = secretkey

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

        self.user_name = username
        self.access_key = accesskey['AccessKey']['AccessKeyId']
        self.secret_key = accesskey['AccessKey']['SecretAccessKey']

    def delete_user(self, username, accesskeyid):
        """Delete a given k8s-console user."""
        self.delete_access_key(username, accesskeyid)
        self.iam_client.delete_user(UserName=username)
