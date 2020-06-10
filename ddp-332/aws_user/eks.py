# -*- coding: utf-8 -*-

"""Classes for EKS."""

import subprocess
import shlex


class EksManager:
    """Manage AWS IAM Identity Mappings."""

    def __init__(self, clustername):
        """Create a UserManager object."""

        self.clustername = clustername

    @staticmethod
    def run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        """Execute os command."""
        process = subprocess.run(
            command,
            stdout=stdout,
            stderr=stderr,
            universal_newlines=True,
            check=True
        )

        if process.stdout:
            print(process.stdout)
        else:
            print(process.stderr)

    def create_iamidentitymapping(self, username, userarn):
        """Add IAM identity to configmap aws-auth."""
        command = shlex.split("eksctl create iamidentitymapping --cluster %s --arn %s --username %s" % (self.clustername, userarn, username))

        self.run(command)

    def delete_iamidentitymapping(self, userarn):
        """Delete IAM identity to configmap aws-auth."""
        command = shlex.split("eksctl delete iamidentitymapping --cluster %s --arn %s" % (self.clustername, userarn))

        self.run(command)
