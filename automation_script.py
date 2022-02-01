"""
This is testing script for the first part of my aws project.
"""
import os
import time
import subprocess
import zipfile
import logging

"""
Global Constants
"""
logval="aws logs describe-log-streams --log-group-name '/aws/lambda/lambdaProjectfunction' --query 'logStreams[*].logStreamName' --max-items 1 --order-by LastEventTime --descending" 
getlog = "aws logs get-log-events --log-group-name '/aws/lambda/lambdaProjectfunction' --log-stream-name"
upload_lambda = "aws lambda update-function-code --function-name lambdaProjectfunction --zip-file fileb://function.zip"
run_lambda = "aws lambda invoke \
        --function-name lambdaProjectfunction \
        --payload '{ \"Body\": \"PUT My cat is beautiful.\", \"fromNumber\" : \"6266241275\", \"image\": \"https://s3.amazonaws.com/mturk-s3-demo/abbey.jpg\", \"numMedia\" : \"1\" }' \
        response.json"

file_content = [
        "bin",
        "certifi",
        "certifi-2021.10.8.dist-info",
        "charset_normalizer",
        "charset_normalizer-2.0.10.dist-info",
        "idna",
        "idna-3.3.dist-info",
        "requests",
        "requests-2.27.1.dist-info",
        "urllib3",
        "urllib3-1.26.8.dist-info",
        "lambda_function.py"
]

"""
Helper Functions
"""
def zip_dir(path, zip_file):
    #os.walk is walking the entire tree
    # root will change to all subfolders
    for root, dirs, files in os.walk(path):
        for file in files:
            #we are adding paths and files to the zip
            zip_file.write(os.path.join(root, file))

def create_lambda_zip(zip_file_content_list,zip_name):
    zip_file = zipfile.ZipFile(zip_name, 'w')
    for path in zip_file_content_list:
        print("path",path)
        if os.path.isdir(path):
            zip_dir(path, zip_file)
        else:
            zip_file.write(path)
    zip_file.close()


def main():


    #check if file exists
    if os.path.exists("lambda_function.py") == True:
        print("lambda function python file exists and uploading to AWS")
        #create zipfile
        #ToDo: add functionality to add folders along with thier files to zip
        create_lambda_zip(file_content,"function.zip")
        #upload to AWS
        upload_process = subprocess.run(upload_lambda,shell=True,capture_output=True,text=True)
        print(upload_process.stdout)
    else:
        print("lambda function python file doesn't exist")

    #run the lambda function with test JSON
    run_lambda_process = subprocess.run(run_lambda,shell=True,capture_output=True,text=True)
    print(run_lambda_process.stdout)

    print("Program is Entering sleep so lambda can upload to cloud watch")
    time.sleep(15)

    #get most recent logs
    log_val_process = subprocess.run(logval,shell=True,capture_output=True,text=True)
    log_stream_val = log_val_process.stdout.strip("[\n]").replace('"',"\'")

    print(log_stream_val)

    #need to add wait so that logs make it to AWS before display
    display_process= subprocess.run(getlog + log_stream_val,shell=True,capture_output=True,text=True)
    print(display_process.stdout)

main()