from urllib.request import urlopen
from bs4 import BeautifulSoup

# News class
class News:
    # constructor.
    # params:
    #   title - news title <string>
    #   content - news content <string>
    def __init__(self, title, content):
        self.title = title
        self.content = content

# Event class
class Event:
    # constructor.
    # params:
    #   title - event title <string>
    #   month - event month. e.g "June" <string> 
    #   day - event date. e.g "10" <string>
    #   time - event time. e.g. "7:15 PM" <string>
    def __init__(self, title, month, day, time = ""):
        self.title = title
        self.month = month
        self.day = day
        self.time = time

# Marlboro public school web page scraping class
class MPSWeb:
    HOME_URL = "https://www.mtps.org/" # home page url
    MONTH_DICT = {'Jan':'January',
                      'Feb':'Febuary',
                      'Mar':'March',
                      'Apr':'April',
                      'May':'May',
                      'Jun':'June',
                      'Jul':'July',
                      'Aug':'August',
                      'Sep':'September',
                      'Oct':'October',
                      'Nov':'November',
                      'Dec':'December'}    

    # constructor.
    # Download home page and cood soup
    def __init__(self):
        with urlopen(MPSWeb.HOME_URL) as req:
            self._soup = BeautifulSoup(req, "html.parser")

    # Return a list of news found on MPS home page.
    # Each element of the list is a News object.
    def getAllNews(self):
        #Soup already cooked in self._soup :)
        ret = []
        newsSoup = self._soup.select('#index_news article')
        for news in newsSoup:
            newsTitle = news['aria-label']
            newsContent = news.select('.item-text')[0].text.strip()
            if newsContent == '':
                newsContent = newsTitle
            elif newsTitle != newsContent:
                newsContent = newsTitle + ". " + newsContent
            ret.append(News(newsTitle, newsContent))
        return ret

     # Return a list of events found on MPS home page.
    # Each element of the list is an Event object
    def getAllEvents(self):
        #Soup already cooked in self._soup :)
        ret = []
        eventSoup = self._soup.select('#index_events article')
        for event in eventSoup:
            eventTitle = event.select('.item-name')[0].text.strip()
            eventMonth = self.translateMonth(event.select('.event-month')[0].text.strip())
            eventDay = event.select('.event-day')[0].text.strip()
            selectTime = event.select('.event-time')
            eventTime = ""
            if selectTime: # If time presented
                eventTime = selectTime[0].text.strip()
                eventTime = eventTime.split(":")[-1] # remove "Time: " in front
            ret.append(Event(eventTitle, eventMonth, eventDay, eventTime))
        return ret
    
    def translateMonth(self,month):
        if month in MPSWeb.MONTH_DICT:
            return MPSWeb.MONTH_DICT[month]
        else:
            return month
# Inline testing
if __name__ == "__main__":
    mps = MPSWeb()
    print("Here are the latest news for marlboro public school: ")
    print("===============================")
    for news in mps.getAllNews():
        print("Title [%s]. Content [%s]" % (news.title, news.content))

    print("\n\n")
    print("Here are the latest events for marlboro public school: ")
    print("===============================")        
    for event in mps.getAllEvents():
        print("Title [%s]. Date-Time [%s %s %s] " % (event.title, event.month, event.day, event.time))


