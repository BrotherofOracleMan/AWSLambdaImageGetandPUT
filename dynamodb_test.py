from ast import Expression
import boto3

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

def update_item(search_key,new_file_name,newDescription,newphoneNumber,newpublicURL,dynamo_db=None):
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

#driver for code

def main():
    dynamodb = boto3.resource('dynamodb')
    searchkey={"filename":"abbey.jpg"}
    newKey = {"filename":"abbey.jpg","phoneNumber":"6266241275", "Description":"My beautiful Cat","publicURL":"https://projectbucketimageupload.s3.us-west-2.amazonaws.com/download.jpg"}
    update_Key={"filename":"abbey.jpg","phoneNumber":"6266241275", "Description":"A black cat","publicURL":"https://projectbucketimageupload.s3.us-west-2.amazonaws.com/download.jpg"}
    search_update_key = {"filename":"abbey.jpg", "Description":"My beautiful Cat","phoneNumber":"6266241275","publicURL":"https://projectbucketimageupload.s3.us-west-2.amazonaws.com/download.jpg"}
    """
    
    if getItem(key=searchkey,dynamodb=dynamodb) != None:
        print("Item exists within the table")
        pass
    else:
        response = put_item(new_key=newKey,resource=dynamodb)
    """
    #print(put_item(new_key=newKey,dynamodb=dynamodb))
    #print(getItem(key=searchkey,dynamodb=dynamodb))
    print(update_item(searchkey,update_Key["filename"],update_Key["Description"],update_Key["phoneNumber"],update_Key['publicURL'],dynamo_db=dynamodb))
main()


