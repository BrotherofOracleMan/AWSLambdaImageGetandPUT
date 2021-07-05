# NotificationBot

![NotificationBotV2 (1)](https://user-images.githubusercontent.com/16285362/124404647-a9904c00-dcf0-11eb-81cb-daa4c84c4f0f.png)


## Components and Functionalities of Projects(Project Design)

### 1) Twilio
Main Functionality: Get User Messages from Twilio Number and send back Messages to Users.
* Output: Send Twilio XML to AWS API Gateway EndPoint 
* Input: Recieve XML from AWS Endpoint to send back to User

### 2) API Gateway SMS Endpoint
Main Functionality: To serve as an enpoint in which Twilio will use to communciate with AWS.
* Output: Send input to Lambda Function.
* Input:  Recieve input from Lambda Function that User request is fufilled

### 3) GatewayToLex Lambda
Main Functionality: To translate input from our Gateway endpoint and send it to the Lex Bot. We also get the output(a confirmation message to confirm transaction waqs done) from the Lex Bot and send it back to user(either through AWS chain or through twilio directly).
* Output: Input to Lex Bot make sure this is a string
* Input: Output from the Lex Bot

### 4) LexBot
Main Functionality: The actual bot that will take read input and fufill a request according to what the user wants
* Output: Output to Lambda (Fufillment request)
* Input: Output from the Lex Bot

### 5) LexToDynamoDB Lambda
Main Functionality: Handles Fufillment request from the LexBot. It is either read a event or write a future event.
* Output: Notify Success to Lex successful fufillment
* Input: Read Database and recieve fufillment requests

### 6)DynamoDB Database
Main Functionality: Serve as DataBase for Lambdas to fetch or write data
* Output: None
* Input: None

### 7)Polling Lambda
Main Functionality: Polls DataBase for events that need to happen everyminute
* Output: direct message to Twilio if event happened
* Input: DataBase

## Tasks to do (Basic Functionalities)

- [X] Get Twilio to communicate with AWS
- [ ] Get Basic Bot working with the four basic requests and reject certain output
- [ ] User requests to put Remind me to carve pumpking at 7pm toay
- [ ] User requests to change time for Certain Event
- [ ] User can cancel events
- [ ] User can ask for a remind me for all events for a the Day
- [ ] Connect Bot to Twilio communication and work other communication
- [ ] Test Using SMS


## Tasks to do (Extra Functionalities)
- [ ] Make a subscribe/unsubscribe functionality
- [ ] Can schedhule Multiple events: Remind me for entire week at 7pm to do a certain thing



