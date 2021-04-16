from fastapi import APIRouter
from typing import Optional
import requests
import boto3
from urllib.parse import urlparse

router = APIRouter()


@router.get("/api2")
async def getedgardata(url:str):
    string=url

    o = urlparse(string, allow_fragments=False)

    s3 = boto3.client('s3',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
    s3_object = s3.get_object(Bucket=o.netloc, Key=o.path.lstrip('/'))
    body = s3_object['Body']
    client = boto3.client('comprehend',region_name='us-east-1',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
    string=body.read().decode('utf-8')
    entitylist=[]

    for line in string.split('\n\n'):

        response2 = client.detect_pii_entities(
            Text=line,
            LanguageCode='en'
        )
        entitylist.append(response2["Entities"])
    final_list=[item for sublist in entitylist for item in sublist]

    entity_dict={'Entities':final_list}
    return entity_dict
