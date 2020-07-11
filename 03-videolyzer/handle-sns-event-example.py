# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:130501856785:handleLabelDetectionTopic:f75ea410-4173-48d3-88fe-eb9782ac6b7c', 'Sns': {'Type': 'Notification', 'MessageId': '0f1a4b73-d232-5476-8ad4-1cf00c0d0d8b', 'TopicArn': 'arn:aws:sns:us-east-1:130501856785:handleLabelDetectionTopic', 'Subject': None, 'Message': '{"JobId":"620fc5a9881b467dcd7f7160c28e61e2fd311e3add36f6ee9e25d0bd6cbe00d8","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1594481663318,"Video":{"S3ObjectName":"balloons.mp4","S3Bucket":"python-automation-themightylaz-videolyzer-videos"}}', 'Timestamp': '2020-07-11T15:34:23.372Z', 'SignatureVersion': '1', 'Signature': 'i6zEbOYnS7gtgQgYZutTV3EXPIXLvD7sUCbZGzZnbvgJ/CFTl13kKe+Vl77Wt1w6rN2/UWHfZhJCNnHWiHLz/44yCuKP4ClKQxKswbJmzpvKk8n1Gf+MRGnpOmXqNREi57pb4y2Qpxc9hn0r+5KcLRlTEyvCQX+Y+TzfCBoRFrmEVJKJRU0UeJVTDkyI8nx0RXc5KeyLoQhTxCjcxthcY1D/NQqLFAjGNH6t70z3ZC/G3qfQVR21oRCZjxsm6/tPcsjEIEQCA+6DtSYHSomSJQnvIA87RbUTBBNKTRRAyx/bXSttRUpwB/nkyvhWcIhnkeyll6gV45QROh5NsGjKhA==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:130501856785:handleLabelDetectionTopic:f75ea410-4173-48d3-88fe-eb9782ac6b7c', 'MessageAttributes': {}}}]}
event
event.keys()
event['Records'][0]
event['Records'][0].keys()
event['Records'][0]['EventSource']
event['Records'][0]['EventVersion']
event['Records'][0]['EventSubscriptionArn']
event['Records'][0]['Sns']
event['Records'][0]['Sns']['Message']
event['Records'][0]['Sns']['Message']['JobId']
type(event['Records'][0]['Sns']['Message'])
import json
json.loads(event['Records'][0]['Sns']['Message'])
