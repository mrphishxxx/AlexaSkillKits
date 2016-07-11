import requests
from bs4 import BeautifulSoup

def google_search(query_term):
	html = ''
	try:
		html = requests.get('https://www.google.com/search?q=' + query_term).text
	except:
		print("can not access google")
	if html is not '':
		links = []
		soup = BeautifulSoup(html, 'html.parser')
		results = soup.find("div", {"id": "resultStats"})
		print "There are " + results.getText() + " returned from google"
		print "here are some examples: "
		for link in soup.find_all('a'):
			url = str(link.get('href'))
			if '/url?' in url:
				text = link.getText()
				if str(text) != '' and 'Cached' not in text :
					print link.getText()
					links.append(url)
		links = set(links)

if __name__ == '__main__':
	print 'example search for term "obama"'
	google_search("obama")