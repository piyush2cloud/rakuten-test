from database import videoHelper
from response import responseBuilder
import json
import os


def handler(event, context):
    try:
        # getting packageId and returning video information from it:
        packageId = getParamsValue("packageId", event)
        videoMetadata = videoHelper.readVideoData('packageId', str(packageId), os.environ["DYNAMO_TABLE_ENCODER_NAME"])
    except Exception as e:
        return responseBuilder.buildResponse(500, json.dumps({'error': str(e)}))
    return responseBuilder.buildResponse(200, json.dumps(videoMetadata))


def getParamsValue(keyName, event):
    return event["pathParameters"][keyName]
