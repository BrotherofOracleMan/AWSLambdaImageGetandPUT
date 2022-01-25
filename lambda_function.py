import boto3

def lambda_handler(event, context):
	print("This event is being tested")
	#unparse event from JSON to dictionary. This dictionary will be in the form of Body, Number , Image, and number of Media.
	#check the body 


	"""
	Do verification here and do parsing here
	Instruction (Get from 1st word)
	Description (Get from 2nd word to end with period)
	Single Image
	"""

	"""
	PUT
	We should try to put an Image into s3 and dynamodb. 
	- We need to create a s3 url from the image
	"""
	



	"""
	GET
	"""


	return {'Status': 'Lambda is updated'}