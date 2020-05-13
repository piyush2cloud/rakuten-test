from response.responseBuilder import ResponseManager
import json
import boto3
import os

def handler(event, context):
    #response handler for returning responses
    responseHandler = ResponseManager()
    try:
        fileKey= getParamsValue('fileKey', event)
        s3 = boto3.client('s3')
        resp=s3.generate_presigned_post(
            os.environ["BUCKET_NAME"],
            str(fileKey),
            Fields = {"acl": "public-read", "Content-Type": 'video/mp4'},
            Conditions = [
                {"acl": "public-read"},
                {"Content-Type": 'video/mp4'}
            ],
            ExpiresIn=1000
        )
    except Exception as e:
        return responseHandler.buildResponse(500, json.dumps({'error':str(e)}))
    return responseHandler.buildResponse(200, json.dumps(resp))

def getParamsValue(keyName, event):
    return event["queryStringParameters"][keyName]