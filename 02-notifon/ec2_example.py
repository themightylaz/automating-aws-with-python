# coding: utf-8
session = boto3.Session(profile_name='pythonAutomation')
import boto3
session = boto3.Session(profile_name='pythonAutomation')
ec2 = session.resource('ec2')
key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key
type(key)
key.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
    
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cat', 'python_automation_key.pem')
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
import os, stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
ec2.images.filter(Owners=['amazon'])
key
json(key)
list(ec2.images.filter(Owners=['amazon']))
len(list(ec2.images.filter(Owners=['amazon'])))
img = ec2.Image('ami-922914f7')
img.name
ami_name = img.name
ami_name
filters = [{'Name:': 'name', 'Value': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
filters = [{'Name:': 'name', 'Values': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
filters = [{'Name': 'name', 'Values': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
img
key
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances
ec2.Instance(id='i-0ceb65fd045592d32')
inst = instances[0]
inst
inst.terminate()
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
inst = instances[0]
inst
inst.public_dns_name
inst.wait_until_running()
inst.reload()
inst.public_dns_name
inst.security_groups
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg
sg.authorize_ingress(IpPermissions=[{'FromPort': 22, 'ToPort': 22, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '192.121.200.7/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort': 80, 'ToPort': 80, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
inst.public_dns_name
get_ipython().run_line_magic('history', '')
get_ipython().run_line_magic('save', 'ec2_example.py 1-55')
