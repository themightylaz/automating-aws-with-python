# automating-aws-with-python

Repository for the A Cloud Guru course *Automating AWS with Python*

## 01-webotron

Webotron is a scripts that will sync a local directory
to an S3 bucket, and optionally configure Route 53
and Cloudfront as well.

### Features

Webotron currently has the following features:

- List bucket
- List content of a bucket
- Create and set up bucket
- Sync directory tree to bucket
- Set AWS profile with --profile=<profileName>
- Configure route 53 domain


## 02-notifon

Notifon is a project to notify Slack users of changes to your AWS account
using CloudWatch Events

### features

Notifon currently has the following features:

- Send notifications to Slack when CloudWatch events happen








## ddp-332 (aws_user)

aws-user manages temporary aws and k8s resources for requesting and revoking firefighter access.

### requires

eksctl with environment variable AWS_PROFILE set.

### features

aws-user currently has the following features:
- Generates a k8s-console user
- Deletes expired k8s-console users
- Set AWS profile with --profile=

### example

```
STH-C02XW07UJGH7:ddp-332 larnis$ aws_user
Usage: aws_user [OPTIONS] COMMAND [ARGS]...

  aws-user manages AWS temporary users for firefighter access.

Options:
  --profile TEXT            Use a given AWS profile.
  --kubeconfig TEXT         Use a KUBECONFIG file name.
  --clustername TEXT        Use a EKS cluster name.
  --namespace TEXT          Use a K8S namespace.
  --label_selector TEXT     Use a K8S label selector.
  --expire_annotation TEXT  Use a K8S expire annotation.
  --help                    Show this message and exit.

Commands:
  create-temp-aws-k8s-resources     Generate temp firefighter resources.
  delete-expired-aws-k8s-resources  Delete expired firefighter resources.
```

#### create resources

```
STH-C02XW07UJGH7:ddp-332 larnis$ aws_user --profile=d2-k8s-console-user --kubeconfig=config-eks-new-pt1-k8s-console create-temp-aws-k8s-resources
UserName = k8s-console-temp-user-x8yp1gt27u
AccessKeyId = AKIA24ZXC7N32I5NANVX
SecretAccessKey = 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
User k8s-console-temp-user-x8yp1gt27u created.
Role k8s-console-temp-role-b8gphm2824 created.
Role-binding k8s-console-temp-rolebinding-u9xbrkz4tw created.
[ℹ]  eksctl version 0.20.0
[ℹ]  using region eu-central-1
[ℹ]  adding identity "arn:aws:iam::749050461047:user/k8s-console-temp-user-x8yp1gt27u" to auth ConfigMap
```

#### delete expired resources

```
Configmap aws-auth updated with arn:aws:iam::749050461047:user/k8s-console-temp-user-x8yp1gt27u.
STH-C02XW07UJGH7:ddp-332 larnis$
STH-C02XW07UJGH7:ddp-332 larnis$ aws_user --profile=d2-k8s-console-user --kubeconfig=config-eks-new-pt1-k8s-console delete-expired-aws-k8s-resources
Role binding: name=k8s-console-temp-rolebinding-u9xbrkz4tw (namespace=confluent) is expired! Removing it ...
Role binding: name=k8s-console-temp-rolebinding-u9xbrkz4tw (namespace=confluent) is removed!
Role: name=k8s-console-temp-role-b8gphm2824 (namespace=confluent) is expired! Removing it ...
Role: name=k8s-console-temp-role-b8gphm2824 (namespace=confluent) is removed!
User: name=k8s-console-temp-user-x8yp1gt27u is expired! Removing it ...
User: name=k8s-console-temp-user-x8yp1gt27u is removed!
[ℹ]  eksctl version 0.20.0
[ℹ]  using region eu-central-1
[ℹ]  removing identity "arn:aws:iam::749050461047:user/k8s-console-temp-user-x8yp1gt27u" from auth ConfigMap (username = "k8s-console-temp-user-x8yp1gt27u", groups = [])
```

### improvements

Replace usage of eksctl with function kubernetes.patch_namespaced_config_map
