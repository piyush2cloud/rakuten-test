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
    event["body"]=json.loads(event["body"])
    packagingId=event["body"]["packagingId"]
    videoStatus=event["body"]["videoStatus"]
    try:
        videoHelper.updateMediaPackagingData(packagingId, videoStatus)
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps({'error':str(e)}))
    return responseBuilder.buildResponse(200, json.dumps({"message":"success"}))

