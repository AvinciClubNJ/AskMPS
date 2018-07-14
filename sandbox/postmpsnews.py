import mpsweb

import json
import urllib
import uuid
import time

# Post a list of mpsweb.News to web server.
# The content to be posted is in Alex flash briefing json format
#  Param:
#   httpEndpoint - http end point the post request goes to
#   news - a list of mpsweb.News
def postMPSNews(httpEndPoint, newsList):
    # Massage news list to a list of dictionaries according
    # to Alexa flash briefing format requirements
    postNewsList = []
    for news in newsList:
        postNews = {}
        postNews['uid'] = str(uuid.uuid4())
        postNews['updateDate'] = str(time.strftime('%Y-%m-%dT%H:%M:%S.0z'))
        postNews['titleText'] = news.title
        postNews['mainText'] = news.content
        postNewsList.append(postNews)
    
    # post data
    postData = json.dumps(postNewsList, indent=4).encode('utf8')
    req = urllib.request.Request(httpEndPoint, data=postData, headers={'content-type': 'application/json'})
    urllib.request.urlopen(req)


# Main program
mpsWeb = mpsweb.MPSWeb()
postMPSNews('https://aback-lungfish.glitch.me/updatenews', mpsWeb.getAllNews())




