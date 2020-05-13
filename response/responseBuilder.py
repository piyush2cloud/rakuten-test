import json

class ResponseManager:
    def __init__(self):
        super().__init__()

    # define response functions
    def success(self,bodyBuilder):
        return self.buildResponse(200,json.dumps(bodyBuilder))

    def failure(self,bodyBuilder):
        body={
            "errorMessage":bodyBuilder
        }
        return self.buildResponse(500,json.dumps(body))


    def unauthorized(self,bodyBuilder):
        body={
            "errorMessage":bodyBuilder
        }
        return self.buildResponse(403,json.dumps(body))

    def buildResponse(self,statusCode, body):
        return {
            "statusCode":statusCode,
            "headers": { "Access-Control-Allow-Origin" : "*" },
            "body":body
        }
