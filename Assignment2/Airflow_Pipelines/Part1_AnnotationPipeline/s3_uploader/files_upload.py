import boto3
from configparser import ConfigParser
import os
import glob
config = ConfigParser()

def files_upload_edgar():
	config.read('config.ini')
	bucket = config.get('main1', 'bucket')
	filepath = config.get('main1', 'filepath')

	 #upload to s3

	arr = os.listdir(filepath)
	s3 = boto3.resource('s3')

	for file in arr:
		s3.Bucket(bucket).upload_file('{}/{}'.format(filepath,str(file)),'{}/{}'.format('files',str(file)))