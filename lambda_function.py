import boto3
import requests
import logging

"""
	#this function should generate a public url if succuessful, other wise generate a exception
"""
def lambda_handler(event, context):
	#unparse event from JSON to dictionary. This dictionary will be in the form of Body, Number , Image, and number of Media.
	#check the body 
	
	#AWS resources and other variables
	#session initiates aws connection
	#resource grabs the data
	aws_session = boto3.Session()
	s3 = aws_session.resource('s3')
	s3_bucket = s3.Bucket("projectbucketimageupload")

	"""
	Logger setup
	"""
	logger = logging.getLogger("Project lambda function")
	logger.setLevel(logging.INFO)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	"""
	Do verification here and do parsing here
	Instruction (Get from 1st word) (PUT or GET)
	Description (Get from 2nd word to end with period)
	Single Image
	"""
	logger.info("lambda is invoked")


	body = event['Body']
	image_url = event['image']
	phone_number = event['fromNumber']
	numMedia = int(event['numMedia'])

	bodyvalues= body.split()
	instruction = str(bodyvalues[0]).strip()
	description = " ".join([bodyvalues[i] for i in range(1,len(bodyvalues)) if bodyvalues[i] != "."])
	filename = image_url.split("/")[-1]
	
	if instruction != "PUT" and instruction != "GET":
		logger.error("Valid Instruction outside of PUT and GET was recieved")
		return {'Error':'Please put an valid instruction (PUT,GET)'}
	
	if numMedia > 1 or numMedia == 0:
		logger.error("Number of Media is above 1 or is set to zero")
		return {'Error':'Please insert a single image'}


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
		logger.info("PUT is called. Inserting image into s3 bucket and DynamoDb database")
		try:
			r = requests.get(image_url,stream=True)
			#upload_to_S3(aws_session,r.raw,filename)
			s3_bucket.upload_fileobj(r.raw,filename)
			logger.info("Successful upload to s3")
		except Exception as error:
			logger.error("An exception occured while inserting into S3 bucket and DB: {} ".format(error))
		finally:
			logger.info("PUT function is Done")
	"""
	GET
	We should Try to query the DynamoDB database with the Title, and then description.
	If we cannot find it, return Image not Found
	If we find it return a fancier image through the api gateway
	"""
	if instruction == "GET":
		logger.info("Executing GET instruction")

	logger.info("Lambda is done executing")
	print("End of function")
	return {'Status': 'Lambda is finished'}