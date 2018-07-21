import mpsweb
import json
import io

# lambda entry point function.
# event is alex skill input
def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return onLaunch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return onIntent(event["request"], event["session"])

# Laurch request handler
def onLaunch(launchRequest, session):
    return getWelcomeResponse(session)

# Intent request handler
def onIntent(intentRequest, session):
    #intent = intentRequest["intent"]
    intentName = intentRequest["intent"]["name"]
    if 'attributes' not in session:
        session['attributes'] = {}

    if intentName == "MPSNews":
        return getNews(session)
    elif intentName == "MPSEvents":
        return getEvents(session)
    elif intentName == "AMAZON.HelpIntent":
        return getWelcomeResponse(session)
    elif intentName == "AMAZON.FallbackIntent":
        return handleFallback(session)
        return getWelcomeResponse(session)        
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest(session)
    elif intentName == "AMAZON.YesIntent":
        return handleYes(session)
    elif intentName == "AMAZON.NoIntent":
        return handleNo(session)
    else:
        raise ValueError("Invalid intent")

# End session handler
def handleSessionEndRequest(session):
    message = "Thank you for using malboro public school skill.  See you next time!"

    return buildResponse(message, shouldEndSession=True)

# Welcome hanlder
def getWelcomeResponse(session):
    message = "Welcome to marlboro public school skill. " \
                    "You can ask me for latest news, or " \
                    "ask me for upcoming events."
    reprompt = "Please ask me for latest news, or upcoming events " \
                    "For example, news, or upcoming events."
    return buildResponse(message, reprompt=reprompt)

# fallback handler
def handleFallback(session):
    message = "I don't know that. Please ask news or events."
    return buildResponse(message, sessionAttributes=session['attributes'])

# MPSNews intent hanlder
def getNews(session):
    mpsWeb = mpsweb.MPSWeb()
    newsList = mpsWeb.getAllNews()

    speaklet = createNewsSpeaklet(newsList)
    reprompt = "Do you want hear the upcoming events?"
    session['attributes']['newsDelivered'] = True

    return buildResponse(speaklet, 
        reprompt, 
        True, 
        shouldEndSession=shouldEnd(session),
        sessionAttributes=session['attributes'])

# MPSEvents intent hanlder
def getEvents(session):
    mpsWeb = mpsweb.MPSWeb()
    eventList = mpsWeb.getAllEvents()
   
    speaklet = createEventsSpeaklet(eventList)
    reprompt = "Do you want hear the news?"
    session['attributes']['eventsDelivered'] = True

    return buildResponse(speaklet, 
        reprompt, 
        True, 
        shouldEndSession=shouldEnd(session), 
        sessionAttributes=session['attributes'])

# Yes intent hanlder
def handleYes(session):
    if 'newsDelivered' in session['attributes']:
        return getEvents(session)
    else: # 'eventsDelivered' in session.attributes:
        return getNews(session)

# No intent hanlder
def handleNo(session):
    return handleSessionEndRequest(session)

#----------------------------
# Session handling
def shouldEnd(session):
    return 'newsDelivered' in session['attributes'] and 'eventsDelivered' in session['attributes']
#----------------------------


#----------------------------
# speaklet helper routines
def createNewsSpeaklet(newsList):
    strIO = io.StringIO()
    startSpeaklet(strIO)
    for news in newsList:
        addSpeechcon(strIO, "ding dong")
        addParagraph(strIO, news.content)
    endSpeaklet(strIO)
    return strIO.getvalue()

def createEventsSpeaklet(eventList):
    strIO = io.StringIO()
    startSpeaklet(strIO)
    for event in eventList:
        addSpeechcon(strIO, "ta da")
        addParagraph(strIO, event.month + event.day + event.time)
        addParagraph(strIO, event.title)        
    endSpeaklet(strIO)
    return strIO.getvalue()

def startSpeaklet(stringIO):
    stringIO.write('<speak>')

def endSpeaklet(stringIO):
    stringIO.write("</speak>")

def addParagraph(stringIO, message):
    stringIO.write("<p>")
    stringIO.write(message)
    stringIO.write("</p>")

def addSentence(stringIO, message):
    stringIO.write("<s>")
    stringIO.write(message)
    stringIO.write("</s>")

def addSpeechcon(stringIO, speeckcon):
    stringIO.write('<say-as interpret-as="interjection">')
    stringIO.write(speeckcon)
    stringIO.write("</say-as>") 

def createSimpleSpeaklet(message):
    return "<speak>" + message + "</speak>"
#-------------------------------

    

# build alexa skill response
def buildResponse(message, reprompt = "", isSpeaklet=False, shouldEndSession = False, sessionAttributes = {}):
    ret = {
        'version': '1.0',
        "sessionAttributes": sessionAttributes,        
        'response': {
            'outputSpeech': {},
            "reprompt": {
                    "outputSpeech": {}
                },            
            'shouldEndSession': shouldEndSession            
        }
    }

    if isSpeaklet:
        ret['response']['outputSpeech']['type'] = "SSML"
        ret['response']['outputSpeech']['ssml'] = message  
        ret['response']['reprompt']['outputSpeech']['type'] = "SSML"
        ret['response']['reprompt']['outputSpeech']['ssml'] = createSimpleSpeaklet(reprompt)              
    else:
        ret['response']['outputSpeech']['type'] = "PlainText"
        ret['response']['outputSpeech']['text'] = message  
        ret['response']['reprompt']['outputSpeech']['type'] = "PlainText"
        ret['response']['reprompt']['outputSpeech']['text'] = reprompt                 

    return ret
