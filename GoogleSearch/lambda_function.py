"""
Simple Alexa skill that perform google search
"""
from __future__ import print_function
from GoogleSearch import google_search

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
    elif intent_name == "GoogleSearch":
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
    card_title = "Google Search"
    speech_output = "Hello, tell me something you wish to know about. "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I didn't understand what you said. " \
                    "Please tell me something you wish to know about. " \
                    "For example, you can say, " \
                    "Google Search about obama. "

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response(intent, session):
    """Response given when the user asks for help"""
    card_title = "Google Search Help"
    session_attributes = session.get('attributes', {})
    should_end_session = False

    speech_output = "I can help you lookup information about subjects you wish to know about " \
                    "For example, you can say, Google Search about obama. "

    reprompt_text = "Sorry, I didn't understand what you said. " \
                    "Please tell me something you wish to know about. " \
                    "For example, you can say, " \
                    "Google Search about obama. "

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
    speech_output = "Sorry, I didn't understand what you said. " \
                    "Please try again." \
                    "For example, you can say, " \
                    "Google Search about obama. "

    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_information(intent, session):
    """
    The main function that looks up the summary infomation about a subject from google.
    """
    card_title = "Google Search"
    session_attributes = session.get('attributes', {})
    should_end_session = False

    # try to get the summary 
    try: 
    	term = intent['slots']['Term']['value'] 
    	dic, suc, res = google_search(term)
    	speech_output = "Found {} results from google".format(res) 
        print(dic.keys())
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
