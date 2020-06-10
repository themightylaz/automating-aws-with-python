from setuptools import setup

setup(
    name='aws-user',
    version='0.1',
    author='',
    author_email='',
    description='aws-user is a tool to manage k8s-console users in AWS',
    license='GPLv3+',
    packages=['aws_user'],
    url='',
    install_requires=[
        'click',
        'boto3',
        'kubernetes'
    ],
    entry_points='''
        [console_scripts]
        aws_user=aws_user.aws_user:cli
    '''
)
