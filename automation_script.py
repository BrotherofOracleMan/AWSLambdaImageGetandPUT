"""
This is testing script for the first part of my aws project.
"""

import os
import subprocess
from zipfile import ZipFile

logval="aws logs describe-log-streams --log-group-name '/aws/lambda/lambdaProjectfunction' --query 'logStreams[*].logStreamName' --max-items 1 --order-by LastEventTime --descending" 
getlog = "aws logs get-log-events --log-group-name '/aws/lambda/lambdaProjectfunction' --log-stream-name"
upload_lambda = "aws lambda update-function-code --function-name lambdaProjectfunction --zip-file fileb://function.zip"

run_lambda = "aws lambda invoke \
    --function-name lambdaProjectfunction \
    --payload '{ \"Body\": \"PUT Description:My cat is beautiful.\", \"fromNumber\" : \"6266241275\", \"image\": \"http://imgur.com\", \"numMedia\" : \"1\" }' \
    response.json"


#check if file exists
if os.path.exists("lambda_function.py") == True:
    print("lambda function python file exists and uploading to AWS")
    #create zipfile
    with ZipFile('function.zip','w') as myzip:
        myzip.write('lambda_function.py')
    #upload to AWS
    upload_process = subprocess.run(upload_lambda,shell=True,capture_output=True,text=True)
    print(upload_process.stdout)
else:
    print("lambda function python file doesn't exist")

#run the lambda function with test JSON
run_lambda = subprocess.run(run_lambda,shell=True,capture_output=True,text=True)
print(run_lambda.stdout)

#get most recent logs
p1 = subprocess.run(logval,shell=True,capture_output=True,text=True)
log_stream_val = p1.stdout.strip("[\n]").replace('"',"\'")

p2 = subprocess.run(getlog + log_stream_val,shell=True,capture_output=True,text=True)
print(p2.stdout)