from database.dbHelper import DynamoManager
from response.responseBuilder import ResponseManager
import json
import os

def handler(event, context):
    #response handler for returning responses
    responseHandler = ResponseManager()
    #Dynamo Db helper functions
    dbHelper=DynamoManager()
    try:
        # getting packageId and returning video information from it:
        packageId = getParamsValue("packageId", event)
        videoMetadata = dbHelper.readVideoData('packageId', str(packageId), os.environ["DYNAMO_TABLE_ENCODER_NAME"])
    except Exception as e:
        return responseHandler.buildResponse(500, json.dumps({'error': str(e)}))
    return responseHandler.buildResponse(200, json.dumps(videoMetadata))


def getParamsValue(keyName, event):
    return event["pathParameters"][keyName]
