import pytest
import os
from .requestFixtures import fetchS3Presigned, getVideoDataInfo, getIncorrectVideoData
import sys
import fetchPresigned
import videoHelper

# #Setting up all the Fixtures to setup Environment Variables.
@pytest.fixture
def set_environment_fixtures():
    os.environ['BUCKET_NAME'] = "rakuten-prod-video-data"
    os.environ[''] = "prod"
    os.environ["DYNAMO_TABLE_ENCODER_NAME"] = "PROD.VIDEO.STATUS.ENCODING"
    os.environ["DYNAMO_TABLE_NAME"] = "PROD.VIDEO.DATA"
    return True


def test_fetch_presigned_url(set_environment_fixtures):
    assert fetchPresigned.handler(fetchS3Presigned(), True)['statusCode'] == 200, "TEST PASSED"
    assert fetchPresigned.handler(fetchS3Presigned(), True)['statusCode'] == 200, "TEST PASSED"


def test_getVideo_Data(set_environment_fixtures):
    assert getVideoData.handler(getVideoDataInfo(), True)['statusCode'] == 200, "TEST PASSED"
    assert getVideoData.handler(getIncorrectVideoData(), True)['statusCode'] == 500, "TEST FAILED"


