import requests

import boto3
import requests
import shutil

"""
	#this function should generate a public url if succuessful, other wise generate a exception

"""
def lambda_handler(event, context):
	
	aws_session = boto3.Session()
	s3 = aws_session.resource('s3')
	s3_bucket = s3.Bucket("projectbucketimageupload")
	
	image_url = "https://s3.amazonaws.com/mturk-s3-demo/abbey.jpg"
	
	r = requests.get(image_url,stream=True)
	
	s3_bucket.upload_fileobj(r.raw,"download.jpg")
	
	return {'Status': 'Lambda is updated'}