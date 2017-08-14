import lxml.html
import time
import traceback
import sys
from selenium import webdriver

def isArrowUrl(url):
	if 'amazon' in url :
		return False
	elif 'rakuten' in url:
		return False
	elif 'yomereba.com' in url:
		return False
	elif 'gnavi.co.jp' in url:
		return False
	elif 'd.hatena.ne.jp/keyword' in url:
		return False
	else:
		return True


class TopPageCrawler:
	"""docstring for TopPageCrawler
		トップページのリンク洗い出し
	"""
	def __init__(self,rootUrl):
		self.urlList = []
		self.topPageUrl = rootUrl

	def addUrls(self,urlList):
		for url in urlList:
			self.addUrl(url)

	def addUrl(self,url):
		urlEle = SimpleUrlElement(url)
		if isArrowUrl(urlEle.url):
			if urlEle not in self.urlList:
				self.urlList.append(urlEle)

	def findLink(self,webDriver):
		try:
			webDriver.get(self.topPageUrl)
			links = lxml.html.fromstring(webDriver.page_source).cssselect('#container .row #main #hotentry a')
		except Exception:
			print('Exception!')
			#raise e
		try:
			self.addUrls(links)
			time.sleep(1)
			links = lxml.html.fromstring(webDriver.page_source).cssselect('#container .row #main #hottopic a')
			self.addUrls(links)
		except Exception:
			print('Exception!')
			#raise e
		try:
			time.sleep(1)
			links = lxml.html.fromstring(webDriver.page_source).cssselect('#container .row #main #category #category-tech a')
			self.addUrls(links)
		except Exception:
			print('Exception!')
			#raise e

class ContentPageCrawler:
	"""docstring for ContentPageCrawler
		コンテンツページのリンク洗い出し
	"""
	def __init__(self, depth):
		self.maxDepth = depth
		self.urlList = []
		print('ContentPageCrawler object maked & maxDepth>>' + str(self.maxDepth))

	def addUrls(self,urlList):
		for url in urlList:
			self.addUrl(url)

	def addUrl(self,url):
		urlEle = SimpleUrlElement(url)
		if isArrowUrl(urlEle.url):
			print('###########'+urlEle.url)
			if urlEle not in self.urlList:
				self.urlList.append(urlEle)

	def findLink(self,targetUrl,webDriver):
		print('findLink!')
		time.sleep(1)
		try:
			webDriver.get(targetUrl)
			print('start! looking for a tag')
			links = lxml.html.fromstring(webDriver.page_source).cssselect('#container #content #wrapper #main .entry-content a')
			print('find urls>>' + str(len(links)))
			self.addUrls(links)
		except Exception:
			ex, ms, tb = sys.exc_info()
			print('Exception!')
			print(ex)
			print(ms)
			print(tb)
			return
			#raise
		finally:
			#webDriver.close()
			print('final')

	def crawl(self,urls,webDriver,depthLevel=0):
		if depthLevel < self.maxDepth:
			print('depthLevel>>' + str(depthLevel))
			print('url length>>' + str(len(urls)))
			for url in urls:
				print('now crawling>>' + url.url)
				self.findLink(url.url,webDriver)
				childPageUrl = ContentPageCrawler(self.maxDepth)
				childPageUrl.crawl(self.urlList,webDriver,depthLevel+1)


class SimpleUrlElement:
	"""docstring for SimpleUrlElement
		urlを管理するクラス
	"""
	def __init__(self,urlEle):
		self.url = urlEle.get('href')
		self.text = str(urlEle.text).strip()
		print('txt>>' + str(self.text))


root_url = 'http://hatenablog.com/'

print('Crawl Start!')
driver = webdriver.PhantomJS()
driver.set_page_load_timeout(5)

topPageUrls = TopPageCrawler('http://hatenablog.com/')
topPageUrls.findLink(driver)
t_len = len(topPageUrls.urlList)
print('top page url count>>' + str(t_len))

contentPageUrl = ContentPageCrawler(2)
contentPageUrl.crawl(topPageUrls.urlList,driver)
c_len = len(contentPageUrl.urlList)

print(c_len)

f = open('/Users//Projects/Webクローラー/out.txt','w',encoding='utf-8')
f.write(str(time.localtime()))
f.write(str(t_len + c_len))
for t in range(t_len):
	f.write(topPageUrls.urlList[t])

for c in range(c_len):
	f.write(contentPageUrl.urlList[c])

f.close()


