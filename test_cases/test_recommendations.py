import pytest
import sys
import os
import json
import requestFixtures
import random
sys.path.append(os.path.abspath('../functions'))
import videoUploader


# #Setting up all the Fixtures to setup Environment Variables.
@pytest.fixture
def set_environment_fixtures():
    os.environ['COMPAIGN_ARN']="arn:aws:personalize:us-east-1:053866237477:campaign/"
    os.environ['STAGE_LEVEL']="release"
    os.environ['PERSONALIZE_BUCKET_NAME']="personalize-viewlift"
    os.environ['TRACKING_ID']="55414609-aba9-448a-8dd3-04e9e0a5df74"
    os.environ['MAIN_JSON_URL']="https://appcms.viewlift.com/"
    os.environ['DYNAMO_TABLE_NAME']="RELEASE.CONTENT.SITE_CONFIG"
    os.environ['AWS_DEFAULT_REGION']="us-east-1"
    os.environ['MEDIA_TYPE_VALUE']="series"
    os.environ['LICENSE_TABLE']="RELEASE.CONTENT.LICENSES"
    os.environ['IAM_ROLE']="arn:aws:iam::053866237477:role/api_lambda_role"
    os.environ['MEDIA_TYPE_LIMIT']="12"
    os.environ['PERSONALIZE_CONFIG_NAME']="personalize-config.json"
    os.environ['MEDIA_TYPE_LIMIT_VAL']="28"
    return True

def test_get_recommendations(set_environment_fixtures):
    assert getRecommendations.handler(requestFixtures.requestGetNoKeyRecommendations("personal"), True)['statusCode']==403,"TEST FAILED"
