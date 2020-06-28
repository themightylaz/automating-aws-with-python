# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
from pathlib import Path
pathname = '~/dev/codebase/automating-aws-with-python/03-videolyzer'
path = Path(pathname).expanduser().resolve()
print(path)
pathname = '~/dev/codebase/automating-aws-with-python/03-videolyzer/video.mp4'
path = Path(pathname).expanduser().resolve()
print(path)
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(Video={'S3Object': {'Bucket': bucket.name, 'Name': path.name}})
bucket = s3.Bucket('pythonautomationvideolyzervideos')
response = rekognition_client.start_label_detection(Video={'S3Object': {'Bucket': bucket.name, 'Name': path.name}})
response
job_id = response['JobId']
result = rekognition_client.get_label_detection(JobId=job_id)
result
result.keys()
result['JobStatus']
result['ResponseMetadata']
result['VideoMetadata']
result['Labels']
len(result['Labels'])
