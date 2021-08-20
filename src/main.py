import json
from datetime import * 
from dateutil.parser import * 
import os
import time
import logging


logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

#-----My personal Helper functions --------#
#should return 
def buildValidationresult(result,violatedSlot, message):
    if result is False:
        return{
            "isValid": result,
            "violatedSlot": violatedSlot,
            "message": {'contentType': 'PlainText', 'content': message}
        }
    
    return {
        "isValid": result,
        "message": {'contentType': 'PlainText', 'content': message}
    }


def CheckDate(Date):
    #Check if Date is valid
    #Check if Date is greater than today 
    datetime_object = None
    if Date is not None:
      logger.info("Validating date")

    try:
        datetime_object = isoparse(Date)
    except ValueError:
        logger.error("Value Error is called Date is invalid")
        return False, 'Date is Invalid. Please enter a Valid Date' 
    
    if datetime_object.date() < datetime.today().date():
        logger.error("Date is in the past")
        return False , 'Date should be before. Re enter a event date that is Today or after'
    
    return True,"Valid Date Given"


def CheckTime(Date,time):
    #Check if time is valid
    #Check if Date is valid
    #if both are valid compare it todays time and
    datetime_object = None
    logger.info(Date)
    try:
        if Date is not None:
            datetime_object = parse(Date)
            logger.info(datetime_object)
        else:
            raise ("Date error")
    except ValueError:
        logger.error("Invalid time was given. Re Enter a valid time")
        return False, "Re-enter Valid time"

    if datetime_object < datetime.today():
        logger.error("Past time given")
        return False, "Re-enter a time that is in the future"
    return True, "Valid Time Given"
    
def CheckEvent(Event):
    logger.info("Validating Event field")
    if Event == "":
        return False,"Event cannot be empty"
    return True, "Event is Valid"

    
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

def ValidateCreateEvent(Date,Time,Event):
    #if Date does exist
        #if Date is not valid return false validation result
        #if Date is less than todays date return a false validation resulted
    if Date is not None:
        validation_result,message = CheckDate(Date)
        logger.info(message)

        if not validation_result:
            return buildValidationresult(False,'Date',message)
        
     #if time does exist
        #if time is not valid return a false validation result
        #if Date is Today and Time is less than now return a flase validation result
    if Time is not None:
        validation_result,message = CheckTime(Date,time)
        if not validation_result:
            return buildValidationresult(False,'Time',message)

    #if event is empty
        # return a false validation result
    if Event == "":
        validation_result,message = CheckEvent(Event)
        if not validation_result:
            return buildValidationresult(False,'Event',message)
        
    #return a true validation result
    return buildValidationresult(True,None,None)


def createEvent(intent_request):
    #use a get slots helper function to get data from the slots
    time = getslots(intent_request)['Time']
    date = getslots(intent_request)['Date']
    event = getslots(intent_request)['Event']
    
    #get all the slots as Dict for future validation
    slots = getslots(intent_request)
    # if it is a Dialog code hook in intent request then
        #Call helper function to validate all the slots
    if intent_request['invocationSource'] == 'DialogCodeHook':
        validation_result = ValidateCreateEvent(date,time,event)
           #if validated result is False:
            #set violated slot value to False
            #make a call for elicit slot
        if validation_result['isValid'] is False:
            slots[validation_result['violatedSlot']] = None
            logger.info(validation_result['message'])
            elicit_slot(intent_request['sessionAttributes'],
                        intent_request['currentIntent']['name'],
                        slots,
                        validation_result['violatedSlot'],
                        validation_result['message']
                        )
                        
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    #return a delegate. Delegate should be for the final bot action for validation. Then it will be send for fufillmnent
    return delegate(output_session_attributes,getslots(intent_request))
    
def dispatch(intent_request):
    if intent_request['currentIntent']['name'] == "CreateEvent":
        logger.info("CreateEvent intent recieved")
        return createEvent(intent_request)
    raise Exception(intent_request + "is not supported")

def lambda_handler(event, context):
    # TODO implement
    os.environ["TZ"] = "America/Los_Angeles"
    time.tzset()
    logger.info("Intent recieved from bot" )
    return dispatch(event)
