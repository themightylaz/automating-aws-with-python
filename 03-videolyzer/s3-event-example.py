# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-07-04T14:54:20.484Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDAR4YUEJYIQETG4IETS'}, 'requestParameters': {'sourceIPAddress': '192.121.200.7'}, 'responseElements': {'x-amz-request-id': 'A5F2AEE1A8390C16', 'x-amz-id-2': '+NqgnW9qpwSrOn/8+Op1jmxcTQDooq5y01gp09a8+2JFU75Ku/ImViGWPGOOOynxWC7Qx24NO+QAXrOimp5jafoanxXFO7SS'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'c403df0c-b578-41c4-bed7-4123c011f148', 'bucket': {'name': 'python-automation-themightylaz-videolyzer-videos', 'ownerIdentity': {'principalId': 'A32HPK7887SLRU'}, 'arn': 'arn:aws:s3:::python-automation-themightylaz-videolyzer-videos'}, 'object': {'key': 'town.mp4', 'size': 5645465, 'eTag': 'f414d9de88710b399f302c6c288760d5', 'sequencer': '005F0098167DFBAC11'}}}]}
event
event['Records'][0]
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
