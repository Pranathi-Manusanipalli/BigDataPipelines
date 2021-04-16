from fastapi import APIRouter
import requests
import boto3
from urllib.parse import urlparse

router = APIRouter()


@router.get("/api1")
async def getedgardata(url:str):
    string=url

    o = urlparse(string, allow_fragments=False)

    s3 = boto3.client('s3',
    	 aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
    s3_object = s3.get_object(Bucket=o.netloc, Key=o.path.lstrip('/'))
    body = s3_object['Body']
    # print(body.read())
    return body.read()
    # return {'message':url}