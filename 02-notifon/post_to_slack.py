# coding: utf-8
import requests
url = '' # Replace with Slack webhook URL
data = { "text": "Hello, world." }
requests.post(url, json=data)
