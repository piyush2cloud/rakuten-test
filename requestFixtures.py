def fetchS3Presigned():
    return {
        "headers": {
            "contentType": 'application/json',
            "x-api-key": 'rakuten-prod-key-12345'
        },
        "queryStringParameters": {
            'fileKey': "rakuten-file"
        }
    }


def getVideoDataInfo():
    return {
        "headers": {
            "contentType": 'application/json',
            "x-api-key": 'rakuten-prod-key-12345'
        },
        "pathParameters": {
            "packageId": "8ce41ff6-944d-11ea-ae9c-8a9eb3be82be"
        }
    }


def getIncorrectVideoData():
    return {
        "headers": {
            "contentType": 'application/json',
            "x-api-key": 'rakuten-prod-key-12345'
        },
        "pathParameters": {
            "packageId": "8eef-8e4c77b79073"
        }
    }

def video_upload_info():
    return {
        "headers": {
            "contentType": 'application/json',
            "x-api-key": 'rakuten-prod-key-12345'
        },
        "body": '{"fileName": "test.mp4", "fileType": "video/mp4", "fileSize": "23223232"}'
    }

def corrupt_video_upload_info():
    return {
        "headers": {
            "contentType": 'application/json',
            "x-api-key": 'rakuten-prod-key-12345'
        },
        "body": {
	        "body": '{"fileType": "video/mp4", "fileSize": "23223232"}'
        }
    }