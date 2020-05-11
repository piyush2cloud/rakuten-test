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
import time;
import uuid

def handler(event, context):
    return responseBuilder.buildResponse(200, "piyush")


