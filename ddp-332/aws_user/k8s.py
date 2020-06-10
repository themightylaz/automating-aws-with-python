# -*- coding: utf-8 -*-

"""Classes for Kubernetes."""


import os
import time
import string
from pprint import pprint

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from aws_user.utils import gen_random_string


class K8sManager:
    """Manage configmaps, roles and role-bindings."""

    DAY_AND_NIGHT = 0  # SHOULD BE SET WHEN TESTING DONE: 60 * 60 * 24

    def __init__(self, kubeconfig, namespace, label_selector, expire_annotation):
        """Create a UserManager object."""
        try:
            config.load_kube_config(
                os.path.join(os.environ["HOME"], '.kube/', kubeconfig))
        except FileNotFoundError:
            print('kubeconfig file {} not found.'.format(kubeconfig))

        self.namespace = namespace
        self.label_selector = label_selector
        self.expire_annotation = expire_annotation

        self.now = time.time()
        self.success = 'Success'

        self.v1_api = client.CoreV1Api()
        self.rbac_api = client.RbacAuthorizationV1Api()

    @staticmethod
    def generate_rolename(size=10, chars=string.ascii_lowercase + string.digits):
        """Generate a user name with random suffix."""
        suffix = gen_random_string(size, chars)
        return 'k8s-console-temp-role-' + suffix

    @staticmethod
    def generate_rolebinding_name(size=10, chars=string.ascii_lowercase + string.digits):
        """Generate a user name with random suffix."""
        suffix = gen_random_string(size, chars)
        return 'k8s-console-temp-rolebinding-' + suffix

    def create_k8s_role(self):
        """Create k8s role for temporary user."""
        rules = [
            client.V1PolicyRule(
                [""],
                resources=["*"],
                verbs=["*"],
            ),
            client.V1PolicyRule(
                ["extensions"],
                resources=["*"],
                verbs=["*"],
            ),
            client.V1PolicyRule(
                ["apps"],
                resources=["*"],
                verbs=["*"],
            ),
            client.V1PolicyRule(
                ["monitoring.coreos.com"],
                resources=["*"],
                verbs=["*"],
            ),
            client.V1PolicyRule(
                ["batch"],
                resources=["*"],
                verbs=["*"],
            )
        ]

        role = client.V1Role(rules=rules)

        role_name = self.generate_rolename()

        label_selector = self.label_selector.split('=')

        role.metadata = client.V1ObjectMeta(
            namespace=self.namespace,
            name=role_name,
            labels={label_selector[0]: label_selector[1]},
            annotations={self.expire_annotation: str(int(self.now + self.DAY_AND_NIGHT))}
        )

        self.rbac_api = client.RbacAuthorizationV1Api()

        try:
            self.rbac_api.create_namespaced_role(self.namespace, role, pretty='true')
        except ApiException as e:
            print("Exception when calling RbacAuthorizationV1Api->create_namespaced_role: %s\n" % e)

        return role_name

    def delete_expired_k8s_roles(self):
        """Delete expired k8s namespaced roles."""
        roles = self.rbac_api.list_role_for_all_namespaces(watch=False, label_selector=self.label_selector)

        for role in roles.items:
            role_name = role.metadata.name
            role_namespace = role.metadata.namespace
            expire_timestamp = int(role.metadata.annotations.get(self.expire_annotation, None))

            if expire_timestamp is None:
                print("Role: name={} (namespace={}) does not have {} annotation!".format(role_name, role_namespace, self.expire_annotation))
            elif expire_timestamp < self.now:
                print("Role: name={} (namespace={}) is expired! Removing it ... ".format(role_name, role_namespace))

                role_delete_response = self.rbac_api.delete_namespaced_role(name=role_name, namespace=role_namespace)

                if role_delete_response.status == self.success:
                    print("Role: name={} (namespace={}) is removed!".format(role_name, role_namespace))
                else:
                    pprint(role_delete_response)

    def create_k8s_rolebinding(self, k8s_role, aws_user):
        """Create k8s role-binding for specified role and user."""
        rolebinding_name = self.generate_rolebinding_name()

        label_selector = self.label_selector.split('=')

        role_binding = client.V1RoleBinding(
            metadata=client.V1ObjectMeta(
                namespace=self.namespace,
                name=rolebinding_name,
                labels={label_selector[0]: label_selector[1]},
                annotations={self.expire_annotation: str(int(self.now + self.DAY_AND_NIGHT))}
            ),
            subjects=[
                client.V1Subject(
                    name=aws_user,
                    kind="User",
                    api_group="rbac.authorization.k8s.io"
                )
            ],
            role_ref=client.V1RoleRef(
                kind="Role",
                api_group="rbac.authorization.k8s.io",
                name=k8s_role
            )
        )

        self.rbac_api = client.RbacAuthorizationV1Api()

        try:
            self.rbac_api.create_namespaced_role_binding(namespace=self.namespace, body=role_binding)
        except ApiException as e:
            print("Exception when calling RbacAuthorizationV1Api->create_namespaced_role_binding: %s\n" % e)

        return rolebinding_name

    def delete_expired_k8s_role_bindings(self):
        """Delete expired k8s namespaced role-bindings."""
        role_bindings = self.rbac_api.list_role_binding_for_all_namespaces(watch=False, label_selector=self.label_selector)

        for role_binding in role_bindings.items:
            role_binding_name = role_binding.metadata.name
            role_binding_namespace = role_binding.metadata.namespace
            expire_timestamp = int(role_binding.metadata.annotations.get(self.expire_annotation, None))

            if expire_timestamp is None:
                print("Role binding: name={} (namespace={}) does not have {} annotation!".format(role_binding_name, role_binding_namespace, self.expire_annotation))
            elif expire_timestamp < self.now:
                print("Role binding: name={} (namespace={}) is expired! Removing it ... ".format(role_binding_name, role_binding_namespace))

                role_binding_delete_response = self.rbac_api.delete_namespaced_role_binding(name=role_binding_name, namespace=role_binding_namespace)

                if role_binding_delete_response.status == self.success:
                    print("Role binding: name={} (namespace={}) is removed!".format(role_binding_name, role_binding_namespace))
                else:
                    pprint(role_binding_delete_response)
