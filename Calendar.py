from collections import OrderedDict as OrderedDictionary
import re

class Calendar:

	def __init__(self):

		self.calendar = OrderedDictionary()
		self.calendar['BEGIN'] = 'VCALENDAR'
		self.calendar['VERSION'] = '2.0'
		self.calendar['PRODID'] = '-//Gareth//Tech Vibes Event Scraper 1.0.2//EN'
		self.calendar['METHOD'] = 'PUBLISH'
		self.calendar['END'] = self.calendar['BEGIN']

		self.info = '' # lines of events and venues

	def getString(self):

		calendarString = ''

		for key in self.calendar.keys()[:-1]: # all keys except last one
			value = self.calendar[key]
			calendarString += self.line(key, value)

		calendarString += self.info

		finalKey = self.calendar.keys()[-1] # 'END' key
		finalValue = self.calendar[finalKey]
		calendarString += self.line(finalKey, finalValue)

		return calendarString

	def line(self, key, value):
		return key + ':' + value + '\r\n'

	def mergeWithFile(self, calendarFile):

		lines = calendarFile.readlines()
		i = 0

		while i < len(lines):
			line = lines[i]
			match = re.match('BEGIN:(\S*)', line)
			if match:
				beginValue = match.group(1)
				if beginValue != 'VCALENDAR':
					break
			i += 1

		while i < len(lines):
			line = lines[i]
			match = re.match('END:(\S*)', line)
			if match:
				beginValue = match.group(1)
				if beginValue == 'VCALENDAR':
					break
			self.info += line
			i += 1

	def googleFormat(self):

		searchResults = re.findall('DESCRIPTION:([\s\S]*?)\r\nURL:([\s\S]*?)\r\n',
				self.info)

		for description, url in searchResults:
			self.info = self.info.replace(description, url)

		searchResults = re.findall('LOCATION(;[\s\S]*?):', self.info)

		for venueId in searchResults:
			self.info = self.info.replace(venueId, '')

		searchResults = re.findall('BEGIN:VVENUE[\s\S]*?END:VVENUE\s*',
				self.info)

		for venue in searchResults:
			self.info = self.info.replace(venue, '')

		return self