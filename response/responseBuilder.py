import json

# define response functions
def success(bodyBuilder):
    return buildResponse(200,json.dumps(bodyBuilder))

def failure(bodyBuilder):
    body={
        "errorMessage":bodyBuilder
    }
    return buildResponse(500,json.dumps(body))


def unauthorized(bodyBuilder):
    body={
        "errorMessage":bodyBuilder
    }
    return buildResponse(403,json.dumps(body))

def buildResponse(statusCode, body):
    return {
        "statusCode":statusCode,
        "headers": { "Access-Control-Allow-Origin" : "*" },
        "body":body
    }
