import json
import subprocess
import socket
import os
import sys
import datetime
import plistlib
import glob
import urllib
import collections
import boto3
from subprocess import call
from datetime import datetime
from time import gmtime, strftime
from collections import OrderedDict
from boto3.dynamodb.conditions import Key, Attr


# Create SQS client
sqs = boto3.client('sqs')
queue_url='https://sqs.us-east-1.amazonaws.com/990323715021/sqs-trigger-encoding'

# os.system('open -a Terminal .')

# Receive message from SQS queue
response = sqs.receive_message(
                                QueueUrl=queue_url,
                                AttributeNames=['All'],
                                MaxNumberOfMessages=1,
                                MessageAttributeNames=['All']
                                )
if 'Messages' in response:
    message = response['Messages'][0]
    ReceiptHandle = message['ReceiptHandle']
    messageId=message['MessageId']
    body = message['Body']
    body=json.loads(body)
    print(body)
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=ReceiptHandle
    )
    #print("sh encoderJob.sh " + str(body["videoPath"]) + " " + str(body["key"]) + " " + str(body["kid"]) + " " + str(body["videoId"]))
    subprocess.call("sh encoderJob.sh " + body["videoPath"] + " " + str(body["key"]) + " " + str(body["kid"]) + " " + body["videoId"]+ " " + body["packagingId"], shell=True)
else:
    print("NO MESSAGE IN QUEUE")