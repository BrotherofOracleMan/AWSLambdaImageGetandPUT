from dis import Instruction
import boto3
import requests
import logging

"""
	#this function should generate a public url if succuessful, other wise generate a exception
"""


def put_item(new_key,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    db_table = dynamodb.Table("projectTable")

    response = db_table.put_item(Item=new_key)
    return response

def getItem(key,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    db_table = dynamodb.Table("projectTable")
    response = None
    try:
        response = db_table.get_item(Key=key)
    except Exception as e:
        print(e)
    finally:
        return response

def update_item(search_key,newDescription,newphoneNumber,newpublicURL,dynamo_db=None):
    if not dynamo_db:
        dynamo_db = boto3.resource('dynamodb')
    db_table = dynamo_db.Table("projectTable")
    UpdateExpression ="SET Description=:d ,phoneNumber=:newNumber, publicURL=:npurl"
    ExpressionAttributeValues = {
        ':newNumber':newphoneNumber,
        ':d': newDescription,
        ':npurl':newpublicURL
    }
    print(search_key)
    response = db_table.update_item(
        Key = search_key,
        UpdateExpression = UpdateExpression,
        ExpressionAttributeValues = ExpressionAttributeValues,
        ReturnValues = "UPDATED_NEW"
    )
    return response
    
def init_logger():
	logger = logging.getLogger("Project lambda function")
	logger.setLevel(logging.INFO)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	return logger

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
	logger = init_logger()
	"""
	Do verification here and do parsing here
	Instruction (Get from 1st word) (PUT or GET)
	Description (Get from 2nd word to end with period)
	Single Image
	"""
	logger.info("lambda is invoked")
	logger.info(event)
	body = event['body']
	image_url = event['image']
	phone_number = event['fromNumber']
	numMedia = int(event['numMedia'])

	bodyvalues= body.split()
	instruction = str(bodyvalues[0]).strip()
	logger.info(instruction)

	if instruction == "GET":
		filename = bodyvalues[1]
	else:
		filename = bodyvalues[1]
		if bodyvalues[2] != ".":
			return "<Response><Message><Body>Please put a space and dot after image name to indicate name of filename</Body></Message></Response>"
		description = " ".join([bodyvalues[i] for i in range(3,len(bodyvalues)) if bodyvalues[i] != "."])
		logger.info(f"Image_url:{image_url}")

	if instruction != "PUT" and instruction != "GET":
		logger.error("Valid Instruction outside of PUT and GET was recieved")
		return f"<Response><Message><Body>Please put an valid instruction (PUT,GET)</Body></Message></Response>"
	
	if (numMedia > 1 or numMedia == 0) and instruction == "PUT":
		logger.error("Number of Media is above 1 or is set to zero")
		return f"<Response><Message><Body>Please insert a single image</Body></Message></Response>"

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
		try:
			r = requests.get(image_url,stream=True)
			#upload_to_S3(aws_session,r.raw,filename)
			s3_bucket.upload_fileobj(r.raw,filename,ExtraArgs = {'ContentType': 'image/jpeg'})
			logger.info("Successful upload to s3")
			#generate an S3 URL
			s3_url = "https://projectbucketimageupload.s3.us-west-2.amazonaws.com/" + filename
			filename_search_key = {"filename": filename}
			new_item_key = {"filename":filename,"Description": description,"phoneNumber":phone_number,"publicURL": s3_url}
			if 'Item' in getItem(key=filename_search_key):
				logger.info("Updating entry in DynamoDB DataBase")
				#do an update
				response = update_item(filename_search_key,description,phone_number,s3_url)
				if response == None:
					logger.error("An exception occured when trying to update a item in the DB")
				else:
					return f"<Response><Message><Body>Updated Item with these details \n filename: {filename} \n Description: {description} \n From Phone Number: {phone_number} </Body>\n <Media> {s3_url}</Media></Message></Response>"
			else: 
				response = put_item(new_key=new_item_key)
				logger.info("Putting Entry into DynamoDB Database")
				if response == None:
					logger.error("An exception occured when trying to insert a new item into the DB")
				else:
					return f"<Response><Message><Body>Created new Item with these details \n filename: {filename} \n Description: {description} \n From Phone Number: {phone_number} </Body>\n <Media>{s3_url}</Media></Message></Response>"
		except Exception as error:
			logger.error("An exception occured while inserting into S3 bucket and DB: {} ".format(error))
		finally:
			logger.info("PUT function is Done")
	"""
	GET
	We should Try to query the DynamoDB database with the Title,.
	If we cannot find it, return Image not Foun,
	If we find it return a fancier image through the api gateway
	"""
	if instruction == "GET":
		response = getItem(key={"filename":filename})
		if 'Item' in response.keys():
			logger.info(response)
			filename = response['Item']['filename']
			description = response['Item']['Description']
			phone_number =  response['Item']['phoneNumber']
			Image_url = response['Item']['publicURL']
			#we can try down
			return f"<Response><Message><Body>Entry was found in database with these details \n filename:{filename} \n Description: {description} \n From Phone Number: {phone_number} </Body>\n <Media> {Image_url}</Media></Message></Response>"
		else:
			return f"<Response><Message><Body>File was not found</Body></Message></Response>"

	logger.info("Lambda is done executing")
	return {'Status': 'Lambda is finished'}