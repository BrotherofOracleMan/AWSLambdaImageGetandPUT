import boto3
import requests
import shutil

def lambda_handler(event, context):
	#unparse event from JSON to dictionary. This dictionary will be in the form of Body, Number , Image, and number of Media.
	#check the body 
	
	"""
	Do verification here and do parsing here
	Instruction (Get from 1st word) (PUT or GET)
	Description (Get from 2nd word to end with period)
	Single Image
	"""

	body = event['Body']
	image_url = event['image']
	phone_number = event['fromNumber']
	numMedia = int(event['numMedia'])

	bodyvalues= body.split()
	instruction = str(bodyvalues[0]).strip()
	description = " ".join([bodyvalues[i] for i in range(1,len(bodyvalues)) if bodyvalues[i] != "."])
	filename = image_url.split("/")[-1]

	
	if instruction != "PUT" and instruction != "GET":
		return {'Error':'Please put an valid instruction (PUT,GET)'}
	
	if numMedia > 1 or numMedia == 0:
		return {'Error':'Please insert a single image'}

	#AWS resources
	s3 = boto3.resource('s3')
	"""
	PUT
	We should try to put an Image into s3 and dynamodb. 
	- We need to create a s3 url from the image.
	- After creating an s3 url from the image we should store unstructured data like this:
	- We should try to avoid duplicate Titles 
	Title	Description	  Date  from Number ImageUrl
	- Return an reciept back to the User       
	"""
	if instruction == "PUT":
		print("Executing PUT function")
		
		r = requests.get(image_url,stream=True)
		
		if r.status_code == 200:
			print("Successful Image Download")
			#ToDo: Need to find a way to upload to bucket through image url
			"""
			r.raw.decode_content = True
			#note lambda storage is only good for as long as the lambda executes
			with open(filename,'wb') as f:
				shutil.copyfileobj(r.raw, f)
			s3.meta.client.upload_file(filename, 'projectbucketimageupload', filename)
			"""
		else:
			return {'Status':'Failed to retrieve Image'}
		
	"""
	GET
	We should Try to query the DynamoDB database with the Title, and then description.
	If we cannot find it, return Image not Found
	If we find it return a fancier image through the api gateway
	"""
	if instruction == "GET":
		print("Executing GET instruction")


	return {'Status': 'Lambda is updated'}