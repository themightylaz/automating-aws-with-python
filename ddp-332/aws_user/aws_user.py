#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
aws_user: Manages k8s-console users.

aws-user automates the process of creating and deleteing temporary users.
- Manage temporary users
  - Creating them
  - Deleteing them
  - Listing them
  - Listing details
"""


import boto3
import click

from aws_user.user import UserManager
from aws_user.k8s import K8sManager
from aws_user.eks import EksManager

session = None
user_manager = None
k8s_manager = None
eks_manager = None


@click.group()
@click.option('--profile', default=None, help="Use a given AWS profile.")
@click.option('--kubeconfig', default='config', help="Use a KUBECONFIG file name.")
@click.option('--clustername', default='operator-pt1-kafka', help="Use a EKS cluster name.")
@click.option('--namespace', default='confluent', help="Use a K8S namespace.")
@click.option('--label_selector', default='kindredgroup.com/temp-access-resource=true', help="Use a K8S label selector.")
@click.option('--expire_annotation', default='kindredgroup.com/expireTimestamp', help="Use a K8S expire annotation.")
def cli(profile, kubeconfig, clustername, namespace, label_selector, expire_annotation):
    """aws-user manages AWS temporary users for firefighter access."""
    global session, user_manager, k8s_manager, eks_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)

    user_manager = UserManager(session, label_selector, expire_annotation)
    k8s_manager = K8sManager(kubeconfig, namespace, label_selector, expire_annotation)
    eks_manager = EksManager(clustername)


@cli.command('create-temp-aws-k8s-resources')
def generate_user():
    """Generate temp firefighter resources."""
    user_name, user_arn = user_manager.generate_user()
    print('User {} created.'.format(user_name))

    role_name = k8s_manager.create_k8s_role()
    print('Role {} created.'.format(role_name))

    bind_name = k8s_manager.create_k8s_rolebinding(role_name, user_name)
    print('Role-binding {} created.'.format(bind_name))

    mapping_name = eks_manager.create_iamidentitymapping(user_name, user_arn)
    print('Configmap aws-auth updated with {}.'.format(user_arn))

    return


@cli.command('delete-expired-aws-k8s-resources')
def delete_expired_resources():
    """Delete expired firefighter resources."""
    k8s_manager.delete_expired_k8s_role_bindings()

    k8s_manager.delete_expired_k8s_roles()

    arn_list = user_manager.delete_expired_aws_users()

    for arn in arn_list:
        eks_manager.delete_iamidentitymapping(arn)


if __name__ == '__main__':
    cli()
