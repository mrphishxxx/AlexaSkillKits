import requests
from bs4 import BeautifulSoup
import sys

def get_quote(company_name):
	'''
		perform google search on a given company name ans stock quote
		if the stock price info box appears in the search results page
		then get the stock price and return that number
	'''
	html = ''
	success = False
	result = ''
	try:
		# get the html from search page
		html = requests.get('https://www.google.com/search?q=stock+quote+' + company_name).text
	except:
		print("can not access google")
	if html is not '':
		# parse the html page
		soup = BeautifulSoup(html, 'html.parser')
		# find the most current stock price
		try:
			result = soup.find("span",{"style":"font-size:157%"}).find("b").getText()
			success = True
		except:
			print "can not get quote on the page"

	return success, result

if __name__ == '__main__':
	if len(sys.argv) > 1:
		company_name = str(sys.argv[1])
	else:
		company_name = 'apple'
	print 'example search for ' + company_name
	s, r = get_quote(company_name)
	if s:
		print "the latest stock quote for {} is {}".format(company_name, r)













