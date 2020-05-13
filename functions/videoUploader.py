from database import dbHelper
from response import responseBuilder
import json
import boto3
import os
import base64
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import time
import uuid


def handler(event, context):
    #Converting Event body to Dict Object to Parse
    try:
        event["body"]=json.loads(event["body"])
        BUCKET_NAME=os.environ["BUCKET_NAME"]
        fileName=event["body"]["fileName"] 
        fileType=event["body"]["fileType"]
        fileSize=event["body"]["fileSize"]
        #S3 Path File Name To be Savend in Database for further operation. 
        s3FilePath="https://"+BUCKET_NAME+".s3.amazonaws.com/"+fileName
        #Generating Video ID which will be associated with the content uploaded by the user.
        videoId=str(uuid.uuid1())   
        #write videodata to Dynamo DB
        dbHelper.writeVideoData(videoId, s3FilePath, fileName, fileType, BUCKET_NAME, fileSize)
        outputObject = {
            "videoId":videoId
        }
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps({'error':str(e)}))
    return responseBuilder.buildResponse(200, json.dumps(outputObject))


