import boto3


def getItem(key,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    db_table = dynamodb.Table("projectTable")
    response =db_table.get_item(key)
    return response if response != None else None

def put_item(new_key,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    db_table = dynamodb.Table("projectTable")
    
    pass

#driver for code

def main():
    dynamodb = boto3.resource('dynamodb')
    searchkey={"filename":"abbey.jpg","phoneNumber":"6266241275"}
    newKey = {"filename":"abbey.jpg","phoneNumber":"6266241275", "Description":"My beautiful Cat","publicURL":"https://projectbucketimageupload.s3.us-west-2.amazonaws.com/download.jpg"}
    if getItem(key=None,dynamodb=dynamodb) != None:
        pass
    else:
        if put_item(new_key=newKey,resource=dynamodb) != None:
            #successful
            pass
        else:
            #not succesful
            pass



main()


