import lxml.html
import requests

from selenium import webdriver

#url指定も自動化の必要性あり
target_url = ''

#静的html

#自動化の必要あり
#htmlのmeta tagの文字コードの判別
#req.encodingをmeta tagの文字コードに揃える処理
#

req = requests.get(target_url)
#response header に指定された文字コード
print(req.encoding)
#meta tagに指定された文字コード
req.encoding = 'shift-jis'
print(req.encoding)

#req.encodingに指定された文字コードで文字をレンダリングする
#そのため実際のhtml内の文字コードをreq.encodingに指定する必要あり
target_html = req.text
root = lxml.html.fromstring(target_html)
#text_content()メソッドはそのタグ以下にあるすべてのテキストを取得する
html_text = root.cssselect('#news_body > p')[0].text_content()
print(html_text)
print('#####')

#JSレンダリング後対応
driver = webdriver.PhantomJS()
driver.get(target_url)
rootj = lxml.html.fromstring(driver.page_source)
#links = rootj.cssselect('#relatedNews a')
links = rootj.cssselect('#news_body > p')[0].text_content()
print(links)
for link in links:
	print (link.text)
