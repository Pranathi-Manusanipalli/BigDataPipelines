from fastapi import APIRouter
from fastapi import FastAPI, Query
from typing import Optional
import requests
import boto3
from urllib.parse import urlparse
import uuid
import hashlib
import base64
import os
from typing import List
router = APIRouter()
client = boto3.client('comprehend', region_name="us-east-1",aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')

@router.get("/api3")
async def mask(input,output,anon_entities:List[str]= Query(None),mask_entities:List[str]= Query(None)):

    s3 = boto3.client('s3',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='LfR3OY+MWpXjZ91yTUK8I0MCmsCTOHzoHgAdGaoQ')
    bucket_name=input.split('//')[1].split('/')[0]
    key=input.split('//')[1].replace(bucket_name+'/','')
    source = input.split('//')[1].split('/')[-1]
    s3_object = s3.get_object(Bucket=bucket_name, Key=key)
    body = s3_object['Body']
    string=body.read().decode("utf-8")

    #print(string)
    def deidentify_entities_in_message(message,type):

                salted_entity = message + str(uuid.uuid4())
                hashkey = hashlib.sha3_256(salted_entity.encode()).hexdigest()
                dynamodb = boto3.resource('dynamodb',region_name='us-east-1',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
                table = dynamodb.Table('anonymize_table')
                response = table.put_item(
                    Item={'source':source,'type':type,'Text': message, 'messagekey': hashkey})
                return hashkey
    anon_list=[]

    for line in string.split('\n\n'):
        if line == '':
            break
        response2 = client.detect_pii_entities(
            Text=line,
            LanguageCode='en'

        )



        for dictionary in response2["Entities"]:
            if (dictionary["Type"]  in anon_entities):
                message=line[dictionary["BeginOffset"]:dictionary["EndOffset"]]
                # print(message)
                hashkey=deidentify_entities_in_message(message,dictionary["Type"])
                # print(hashkey)
                line=line.replace(message,hashkey)
        anon_list.append(line)
    with open('/tmp/newfile.txt', 'w') as f:
        for i in anon_list:
            f.write(i + "\n")
    s3 = boto3.resource('s3',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
    s3.Bucket(bucket_name).upload_file('/tmp/newfile.txt', 'api3_anonymized/anonymized.txt')
    # print(anon_list)

    s3 = boto3.client('s3',aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')

    input="s3://prudhvics/api3_anonymized/anonymized.txt"
    output=output

    response = client.start_pii_entities_detection_job(
        InputDataConfig={
            'S3Uri': '{}'.format(input),
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': '{}'.format(output)
        },
        DataAccessRoleArn='arn:aws:iam::727520526624:role/comprehendfullaccess',
        JobName='comprehend-blog-redact-001',
        LanguageCode='en',
        Mode='ONLY_REDACTION',
        RedactionConfig={
            'PiiEntityTypes': mask_entities,
            'MaskMode':  'REPLACE_WITH_PII_ENTITY_TYPE',
            'MaskCharacter': '*'
        },

    )
    return "Data Masked and Anonymized"