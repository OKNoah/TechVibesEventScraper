from urllib import urlopen as openPage
from re import findall as findAll
from bs4 import BeautifulSoup as parse
from Calendar import Calendar

OUTPUT_FILE_NAME = 'iCal.ics'
GOOGLE_OUTPUT_FILE_NAME = 'iCal_Google.ics'

DOMAIN = 'http://www.techvibes.com'
URL = DOMAIN + '/event/vancouver'

page = openPage(URL)
html = parse(page)

pageList = html.find(class_ = 'pagination')
try:
	pageIndex = pageList.find(class_ = 'active').a['title']
	numberOfPages = int(findAll('Page 1 of (\d+)', pageIndex)[0])
except AttributeError:
	numberOfPages = 1

calendar = Calendar()

for pageNumber in range(1, numberOfPages + 1):

	print 'Page', pageNumber

	url = URL + '/' + str(pageNumber)
	page = openPage(url)
	html = parse(page)

	content = html.find(id = 'content')
	eventListings = content.find_all(class_ = 'event')

	for listing in eventListings:

		print ' Listing'

		eventUrl = DOMAIN + listing.header.a['href']
		eventPage = openPage(eventUrl)
		eventHtml = parse(eventPage)

		eventName = eventHtml.h1.text
		iCalTitle = eventName + ' iCal file'
		iCalUrl = DOMAIN + eventHtml.find('a', title=iCalTitle)['href']

		iCalFile = openPage(iCalUrl)
		calendar.mergeWithFile(iCalFile)

outputFile = open(OUTPUT_FILE_NAME, 'w')
outputFile.write(calendar.getString())
outputFile.close()

googleCalendar = calendar.googleFormat()
googleOutputFile = open(GOOGLE_OUTPUT_FILE_NAME, 'w')
googleOutputFile.write(googleCalendar.getString())
googleOutputFile.close()
