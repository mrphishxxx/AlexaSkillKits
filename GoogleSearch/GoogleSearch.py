import requests
from bs4 import BeautifulSoup

def google_search(query_term):
	'''
		perform google search on the given search term
		return 
			1 dictionary: with sample text - url mappings
			2 boolean: indicate whether there are reuslts or not
			3 string: the number of results found by google
	'''
	html = ''
	text_url_dict = dict()
	results_count = ''
	success = False
	try:
		# get the html from search page
		html = requests.get('https://www.google.com/search?q=' + query_term).text
	except:
		print("can not access google")
	if html is not '':
		# parse the html page
		soup = BeautifulSoup(html, 'html.parser')
		# find the number of results returned from google
		results = soup.find("div", {"id": "resultStats"})
		results_count = results.getText().split(" ")[1]
		print "There are " + results.getText() + " returned from google"
		print "here are some examples: "
		# parse the links
		for link in soup.find_all('a'):
			url = str(link.get('href'))
			if '/url?' in url:
				text = link.getText()
				if str(text) != '' and 'Cached' not in text :
					print link.getText()
					text_url_dict[text] = url
	
	success = len(text_url_dict) > 0

	return text_url_dict, success, results_count

if __name__ == '__main__':
	print 'example search for term "obama"'
	google_search("obama")













