import json
import boto3
import requests
import os
import base64
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import responseBuilder
import videoHelper
import time
import uuid

def handler(event, context):
    #Converting Event body to Dict Object to Parse
    event["body"]=json.loads(event["body"])
    BUCKET_NAME=os.environ["BUCKET_NAME"]
    base64Value=event["body"]["base64"] 
    file_content = base64.b64decode(base64Value)
    fileName=event["body"]["fileName"] 
    fileType=event["body"]["fileType"] 
    fileSize=event["body"]["fileSize"]
    print("START")
    #S3 Service for Uploading Video to S3 Env
    s3 = boto3.client('s3')
    ts = str(time.time())
    fileNameS3=ts+"-"+fileName
    #Generating Video ID which will be associated with the content uploaded by the user.
    videoId=str(uuid.uuid1())

    try:
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=fileNameS3, Body=file_content, ACL='public-read')
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps(e))

    #S3 Path File Name To be Savend in Database for further operation.    
    s3FilePath="https://"+BUCKET_NAME+".s3.amazonaws.com/"+fileNameS3
    s3_response["ETag"]=s3_response["ETag"].replace("\"", "")
    #write videodata to Dynamo DB
    videoHelper.writeVideoData(videoId,s3FilePath, fileNameS3, fileType, BUCKET_NAME, fileSize)
    
    outputObject = {
        "videoId":videoId
    }
    return responseBuilder.buildResponse(200, json.dumps(outputObject))


