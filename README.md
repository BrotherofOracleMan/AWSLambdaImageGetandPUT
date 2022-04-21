Text Image AWS Integration Project


Purpose and Introduction 
   This project was created to teach me about AWS and systems integration. 
   In general what this project does is allow a user to send a image along with details. Once the user does this, AWS will store the image in s3 and details in Dynamo DB. The user is then able to fetch the image later on. Note that if a User wants to update an image, the user can upate it by mentioning the filename again with different details and a different image.
   
Examples of Usage
Please take note of spaces when sending messages to your twilio number

Creation(Use PUT cmd)

![Screenshot](create_1.png)

![Screenshot](create_2.png)

Getting the Image(Use GET cmd)

![Screenshot](GET.png)

Updating the Image (USE PUT cmd)

![Screenshot](Update_1.png)

![Screenshot](Update_2.png)


Architecture diagram 
![Screenshot](ImageFetchNoLex.png)

Requirements
* Twilio account 
* AWS account
* Boto3

Guide 

