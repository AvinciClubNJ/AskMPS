from urllib.request import urlopen
from bs4 import BeautifulSoup

with urlopen("https://www.mtps.org/") as req:
    soup = BeautifulSoup(req, 'html.parser')

    newsSoup = soup.select('#index_news article')
    print("News---------------:")
    for news in newsSoup:
        newsTitle = news['aria-label']
        newsContent = news.select('.item-text')[0].text.strip()
        print(newsTitle, newsContent)
    
    eventSoup = soup.select('#index_events article')
    print("Events---------------:")
    for event in eventSoup:
        eventTitle = event.select('.item-name')[0].text.strip()
        eventMonth = event.select('.event-month')[0].text.strip()
        eventDay = event.select('.event-day')[0].text.strip()
        selectTime = event.select('.event-time')
        eventTime = ""
        if selectTime: # If time presented
            eventTime = selectTime[0].text.strip()
        print(eventTitle, eventMonth, eventDay, eventTime)

