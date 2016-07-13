"""
    Simple Alexa skill that send sms to user
"""
from __future__ import print_function
from twilio.rest import TwilioRestClient

account_sid = ""
auth_token = ""
from_num = ""
to_num = ""
# create a client
client = TwilioRestClient(account_sid, auth_token)

# Populate with your Alexa skill's application ID to prevent someone else
# from configuring a skill that sends requests to this function.
# APP_ID = "amzn1.echo-sdk-ams.app.08dea82f-865d-4a35-a734-2f8125680049"

# ------------------------------------------------------------------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    #print("event.session.application.applicationId=" +
    #      event['session']['application']['applicationId'])

    #if APP_ID and event['session']['application']['applicationId'] != APP_ID:
    #    raise ValueError("Invalid Application ID")

    # print(client.base) see if client object is correctly created
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return get_help_response(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return get_cancel_response(intent, session)
    elif intent_name == "SMS":
        return get_information(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """Welcome message when the skill is launched"""
    session_attributes = {}
    card_title = "SMS"
    speech_output = "Hello, I can send you a sms. "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I didn't understand what you said. " 

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response(intent, session):
    """Response given when the user asks for help"""
    card_title = "SMS Help"
    session_attributes = session.get('attributes', {})
    should_end_session = False

    speech_output = "I can send you a sms."

    reprompt_text = "Sorry, I didn't understand what you said. " 

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_cancel_response(intent, session):
    """Response given when the user cancels the skill"""
    card_title = "Goodbye"
    session_attributes = session.get('attributes', {})
    should_end_session = True
    speech_output = "OK, goodbye"
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def error_response(intent, session):
    """Response given when an unexpected error occurs"""
    card_title = "Oops"
    session_attributes = session.get('attributes', {})
    should_end_session = False
    speech_output = "Sorry, I didn't understand what you said. " 

    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_information(intent, session):
    """
    The main function that looks up the summary infomation about a subject from google.
    """
    card_title = "SMS"
    session_attributes = session.get('attributes', {})
    should_end_session = False

    # try to get the summary 
    try: 
    	message_body = intent['slots']['Term']['value'] 
        print(message_body)
        sms = client.messages.create(
            body = message_body,
            to = to_num,
            from_ = from_num) # this is the twilio phone
        print(sms.sid) 
        speech_output = "Please check you phone" 
    except:
        return error_response(intent, session)

    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
