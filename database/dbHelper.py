import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoManager:
    def __init__(self):
        self.dbClient=boto3.resource('dynamodb')

    # Write Video Data into Dynamo DB
    def writeVideoData(self , videoId ,filePath, fileName, fileType, bucketName, fileSize):
        dbClient = self.dbClient
        table = dbClient.Table(os.environ["DYNAMO_TABLE_NAME"])
        table.put_item(Item= {'videoId': videoId,'filePath': filePath, 'fileName': fileName, 'fileType': fileType, 'bucketName': bucketName, 'fileSize': fileSize})

    # Write Video Data into Dynamo DB
    def writeMediaPackagingData(self ,videoId, packageId, videoStatus):
        dbClient = self.dbClient
        table = dbClient.Table(os.environ["DYNAMO_TABLE_ENCODER_NAME"])
        table.put_item(Item= {'packageId': packageId ,'videoId': videoId, 'videoStatus': 'ENCODE_STARTED'})

    # Read Data From Dynamo DB
    def readVideoData(self ,keyName, keyValue, tableName):
        dbClient = self.dbClient
        table = dbClient.Table(tableName)
        response = table.get_item(
            Key={
                keyName : keyValue,
            }
        )
        return response['Item']

    # Updating Video Status Data into Dynamo DB
    def updateMediaPackagingData(self , packageId, videoStatus, dashUri, keyVal, kidVal):
        dbClient = self.dbClient
        table = dbClient.Table(os.environ["DYNAMO_TABLE_ENCODER_NAME"])
        response = table.update_item(
            Key={
                'packageId': packageId
            },
            UpdateExpression="set videoStatus = :r, dashUrl=:d, keyVal=:k, kidVal=:i",
            ExpressionAttributeValues={
                ':r': videoStatus,
                ':d': dashUri,
                ':k': keyVal,
                ':i': kidVal,
            },
            ReturnValues="UPDATED_NEW"
        )
        print(json.dumps(response))

    #Check Media Package has been sent. If already sent no need to send again.
    def isVideoEncoded(self ,videoId):
        dbClient = self.dbClient
        table = dbClient.Table(os.environ["DYNAMO_TABLE_ENCODER_NAME"])
        response = table.query(
            IndexName="videoId-index",
            KeyConditionExpression=Key('videoId').eq(videoId))
        if len(response[u'Items']) > 0:
            return True
        return False