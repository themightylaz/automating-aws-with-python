from setuptools import setup

setup(
    name='aws-user',
    version='0.1',
    author='Lars Nielsen',
    author_email='lars.nielsen@kindredgroup.com',
    description='aws-user is a tool to manage k8s-console users in AWS',
    license='GPLv3+',
    packages=['aws_user'],
    url='https://github.com/themightylaz',
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
