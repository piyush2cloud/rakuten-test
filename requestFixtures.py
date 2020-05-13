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
            "packageId": "60e057f6-94ef-11ea-8e67-4a66e9734edf"
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