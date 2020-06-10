# -*- coding: utf-8 -*-

"""Classes for IAM users."""

import string
import time

from pprint import pprint
from botocore.exceptions import ClientError

from aws_user.utils import gen_random_string


class UserManager:
    """Manage k8s-console temporary users."""

    AWS_TAGS = [{'Key': 'CostCenter', 'Value': 'D2'},
                {'Key': 'Service', 'Value': 'k8s-console'},
                {'Key': 'Team', 'Value': 'DPML'},
                {'Key': 'Department', 'Value': 'Data'},
                {'Key': 'Jira', 'Value': 'DDP-332'}]

    DAY_AND_NIGHT = 0  # SHOULD BE SET WHEN TESTING DONE: 60 * 60 * 24

    def __init__(self, session, label_selector, expire_annotation):
        """Create a UserManager object."""
        self.session = session
        self.label_selector = label_selector
        self.expire_annotation = expire_annotation

        self.now = time.time()
        self.success = 200

        self.iam_client = self.session.client('iam')

    @staticmethod
    def generate_username(size=10, chars=string.ascii_lowercase + string.digits):
        """Generate a user name with random suffix."""
        suffix = gen_random_string(size, chars)
        return 'k8s-console-temp-user-' + suffix

    def get_tags(self):
        """Get aws tags with label_selector included."""
        tags = self.AWS_TAGS

        label_selector = self.label_selector.split('=')
        label_tag = {'Key': label_selector[0], 'Value': label_selector[1]}
        tags.append(label_tag)

        annotation_tag = {'Key': self.expire_annotation, 'Value': str(int(self.now + self.DAY_AND_NIGHT))}
        tags.append(annotation_tag)

        return tags

    def generate_user(self):
        """Generate a k8s-console user."""
        user = self.iam_client.create_user(
            UserName=self.generate_username(),
            Tags=self.get_tags()
        )

        username = user['User']['UserName']
        accesskey = self.iam_client.create_access_key(UserName=username)

        print('UserName = {}\nAccessKeyId = {}\nSecretAccessKey = {}'
              .format(
                  username,
                  accesskey['AccessKey']['AccessKeyId'],
                  accesskey['AccessKey']['SecretAccessKey']
              ))

        return username, user['User']['Arn']

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

    def delete_expired_aws_users(self):
        """Delete expired k8s-console aws users."""
        user_list = self.iam_client.list_users(MaxItems=100)
        arn_list = []

        for user in user_list['Users']:
            user_name = user['UserName']
            user_tags = self.iam_client.list_user_tags(UserName=user_name)
            if {'Key': 'kindredgroup.com/temp-access-resource', 'Value': 'true'} in user_tags['Tags']:
                user_arn = user['Arn']

                for tag in user_tags['Tags']:
                    tag_values = list(tag.values())
                    if tag_values[0] == 'kindredgroup.com/expireTimestamp':
                        expire_timestamp = int(tag_values[1])

                if not expire_timestamp:
                    print("User: name={} does not have {} annotation!".format(user_name, self.expire_annotation))
                elif expire_timestamp < self.now:
                    print("User: name={} is expired! Removing it ... ".format(user_name))
                    accesskeyids = self.iam_client.list_access_keys(UserName=user_name)

                    for accesskeyid in accesskeyids['AccessKeyMetadata']:
                        self.delete_access_key(user_name, accesskeyid['AccessKeyId'])

                    response = self.iam_client.delete_user(UserName=user_name)
                    if response['ResponseMetadata']['HTTPStatusCode'] == self.success:
                        print("User: name={} is removed!".format(user_name))
                    else:
                        pprint(response)

                    arn_list.append(user_arn)

        return arn_list
