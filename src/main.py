import json
from datetime import * 
from dateutil.parser import * 
import os
import time
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#-----My personal Helper functions --------#
#should return 
def buildValidationresult(result,violatedSlot, message):
    if result is False:
        return{
            "isValid": result
            "violatedSlot": violatedSlot
            "message": message
        }
    
    return {
        "isValid": result
        "violatedSlot": None
        "message": message
    }


def CheckDate(Date):
    return True , ""


def CheckTime(Date,time):
    return True , ""
    
def CheckEvent(Event):
    return True, ""
    
def getslots(intent_request):
    return intent_request['currentIntent']['slots']
    
#-----Amazons's Sample Helper function-------#
#Helper functions for
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
    
#--------------Main Lambda functions for validation and Event Creation-----#

def ValdidateCreateEvent(Date,Time,Event):
    #if Date does exist
        #if Date is not valid return false validation result
        #if Date is less than todays date return a false validation resulted
    if Date is not None:
        validation_result,message = CheckDate(Date)
        if not validation_result:
            return buildValidationresult(False,'Date',message)
        
     #if time does exist
        #if time is not valid return a false validation result
        #if Date is Today and Time is less than now return a flase validation result
    if time is not None:
        validation_result,message = CheckTime(Date,time)
        if not validation_result:
            return buildValidationresult(False,'Time',message)

    #if event is empty
        # return a false validation result
    if event is "":
        validation_result,message = CheckEvent(Event)
        if not validation_result:
            return buildValidationresult(False,'Event',message)
        
    #return a true validation result
    return buildValidationresult(True,None,None)


def createEvent(intent_request):
    #use a get slots helper function to get data from the slots
    time = getslots()['Time']
    date = getslots()['Date']
    event = getslots()['Event']
    
    #get all the slots as Dict for future validation
    # if it is a Dialog code hook in intent request then
        #Call helper function to validate all the slots
        
    #if validated result is False:
        #set violated slot value to False
        #make a call for elicit slot
        
    #return a delegate. Delegate should be for the final bot action for validation. Then it will be send for fufillmnent
    return delegate()
    
def dispatch(intent_request):
    if intent_request['currentIntent']['name'] == "CreateEvent":
        logger.info("CreateEvent intent recieved")
        return CreateEvent(intent_request)
    raise Exception(intent_request + "is not supported")

def lambda_handler(event, context):
    # TODO implement
    os.environ["TZ"] = "America/Los_Angeles"
    time.tzset()
    logger.info("Intent recieved from bot" )
    return dispatch(event)
