from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author='Lars Nielsen',
    author_email='nielsen_lars_rudolf@hotmail.com',
    description='Webotron 80 is a tool to deploy static websites to AWS',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/themightylaz/automating-aws-with-python',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)
