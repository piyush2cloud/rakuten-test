import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

class SqsManager:
    def __init__(self):
        self.client = boto3.client('sqs')

    def send_sqs_message(self, msg_body):
        # Send the SQS message 
        sqs_client=self.client
        sqs_queue_url = sqs_client.get_queue_url(QueueName=os.environ["SQS_NAME"])['QueueUrl'] 
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,MessageBody=json.dumps(msg_body)) 
        return msg