import json
import os
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Write Video Data into Dynamo DB
def writeVideoData(videoId ,filePath, fileName, fileType, bucketName, fileSize):
    dbClient = boto3.resource('dynamodb')
    table = dbClient.Table(os.environ["DYNAMO_TABLE_NAME"])
    print(table.table_status)
    table.put_item(Item= {'videoId': videoId,'filePath': filePath, 'fileName': fileName, 'fileType': fileType, 'bucketName': bucketName, 'fileSize': fileSize})

# Write Video Data into Dynamo DB
def writeMediaPackagingData(videoId, packageId, videoStatus):
    dbClient = boto3.resource('dynamodb')
    table = dbClient.Table(os.environ["DYNAMO_TABLE_ENCODER_NAME"])
    print(table.table_status)
    table.put_item(Item= {'packageId': packageId ,'videoId': videoId, 'videoStatus': 'ENCODE_STARTED'})

# Read Data From Dynamo DB
def readVideoData(keyName, keyValue, tableName):
    client = boto3.resource('dynamodb')
    table = client.Table(tableName)
    response = table.get_item(
        Key={
            keyName : keyValue,
        }
    )
    print(response['Item'])
    return response['Item']

# Updating Video Status Data into Dynamo DB
def updateMediaPackagingData(packageId, videoStatus, dashUri):
    dbClient = boto3.resource('dynamodb')
    table = dbClient.Table(os.environ["DYNAMO_TABLE_ENCODER_NAME"])
    response = table.update_item(
        Key={
            'packageId': packageId
        },
        UpdateExpression="set videoStatus = :r, dashUrl=:d",
        ExpressionAttributeValues={
            ':r': videoStatus,
            ':d': dashUri,
        },
        ReturnValues="UPDATED_NEW"
    )
    print(json.dumps(response))

#Check Media Package has been sent. If already sent no need to send again.
def isVideoEncoded(videoId):
    dbClient = boto3.resource('dynamodb')
    table = dbClient.Table(os.environ["DYNAMO_TABLE_ENCODER_NAME"])
    response = table.query(
        IndexName="videoId-index",
        KeyConditionExpression=Key('videoId').eq(videoId))
    if len(response[u'Items']) > 0:
        return True
    return False

def send_sqs_message(msg_body):
    # Send the SQS message
    sqs_client = boto3.client('sqs')    
    sqs_queue_url = sqs_client.get_queue_url(QueueName=os.environ["SQS_NAME"])['QueueUrl'] 
    msg = sqs_client.send_message(QueueUrl=sqs_queue_url,MessageBody=json.dumps(msg_body)) 
    return msg