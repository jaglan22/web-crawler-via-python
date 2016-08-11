# -*- coding: utf-8 -*-



import re,sys,time
reload(sys)
sys.setdefaultencoding( "utf-8" )
from selenium import webdriver


def parsePage(html,ProductlinkSet):
    products=re.finditer('a-text-normal" title="(.*?)" href="(.*?)"><h2',html)
    for product in products:
        ProductlinkSet.add(product.group(2).strip())        

fw=open('Amazonreviews.txt','w') 

revcount=0
name=set()
page=1
while True:
    
    print 'processing page',page 
    
    url='http://www.amazon.com/s/ref=sr_pg_'+str(page)+'?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A1266092011%2Cn%3A172659%2Cp_89%3ASamsung&bbn=1266092011&ie=UTF8&qid=1443822987'
    
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(2)
    
    Productlink=set()
    parsePage(driver.page_source,Productlink)
    
    for link in Productlink:
        print link
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(link)
        button=driver.find_element_by_css_selector('#revF > div > a')
        button.click()
        time.sleep(3)
        
        revs=re.finditer(' review-rating"><span class="a-icon-alt">(.*?)</span></i></a><span class="(.*?)a-size-base a-link-normal author" href="(.*?)">(.*?)</a></span><span class="a-declarative"(.*?)review-date">on (.*?)</span></div><div class=(.*?)class="a-size-base review-text">(.*?)</span></div><',driver.page_source)
        for rev in revs:
            rating=rev.group(1)
            username=rev.group(4)
            date=rev.group(6)
            text=rev.group(8)
            fw.write('amazon.com'+'\t'+text+'\t'+rating+'\t'+date+'\n')
            revcount+=1
       
        
        print 'revpage 1 done ',revcount
        if revcount>=1000:
                break
        
        revpage=2
        while True:
            cssPath='#cm_cr-pagination_bar > ul > li.a-last > a'
            
            
            try:
                button=driver.find_element_by_css_selector(cssPath)
            except:
                error_type, error_obj, error_info = sys.exc_info()
                print 'STOPPING - COULD NOT FIND THE LINK TO PAGE: ', revpage
                print error_type, 'Line:', error_info.tb_lineno
                break
            
            button.click()
            time.sleep(3)
            
            revs=re.finditer(' review-rating"><span class="a-icon-alt">(.*?)</span></i></a><span class="(.*?)a-size-base a-link-normal author" href="(.*?)">(.*?)</a></span><span class="a-declarative"(.*?)review-date">on (.*?)</span></div><div class=(.*?)class="a-size-base review-text">(.*?)</span></div><',driver.page_source)
            for rev in revs:
                rating=rev.group(1)
                username=rev.group(4)
                date=rev.group(6)
                text=rev.group(8)
                fw.write('amazon.com'+'\t'+text+'\t'+rating+'\t'+date+'\n')
                revcount+=1
           
            
            print 'revpage ',revpage,' done ',revcount
            
            revpage+=1
            
            if revcount>=1000:
                break
            
        if revcount>=1000:
                break
        
        
    page+=1
    if revcount>=1000:
        break
    
        
print revcount

   
fw.close()



# -*- coding: utf-8 -*-
'''

BestBuy
'''
import re
import time,sys
from selenium import webdriver
from bs4 import BeautifulSoup
#extract the set of users in a given html page and add them to the given set
fw =  open('result.txt','w')
reviewtext_list=list()
rating_list=list()
date_list=list()
url_list=list()
link_list=list()
page = 1
review_num = 0

def getReview(html):
	soup = BeautifulSoup(html, 'html.parser')
	reviewcontainer_divs = soup.findAll("div",{"class":"BVRRReviewTextContainer"})
	for reviewcontainer_div in reviewcontainer_divs:
		soup = BeautifulSoup(`reviewcontainer_div`, 'html.parser')
		reviewtext_divs = soup.findAll("span",{"class":"BVRRReviewText"})
		temp = ""
		for reviewtext_div in reviewtext_divs:
			temp += reviewtext_div.text
		reviewtext_list.append(temp)

def getRating(html):
	soup = BeautifulSoup(html, 'html.parser')
	rating_divs = soup.findAll("div",{"id":"BVRRRatingOverall_Review_Display"})
	for rating_div in rating_divs:
		ratings = re.finditer('<span class="BVRRNumber BVRRRatingNumber" property="v:value">(.*?)</span>',`rating_div`)
		for rating in ratings:
			rating_list.append(rating.group(1).strip())

def getDate(html):
	review_dates = re.finditer('<span property="v:dtreviewed" content="(.*?)" class="BVRRValue BVRRReviewDate">',html)
	for review_date in review_dates:
		date_list.append(review_date.group(1).strip())

def getItemList(html):
	itemlist = re.finditer('<div class="sku-title" itemprop="name"><h4><a href="(.*?)" data-rank="pdp">',html)
	for item in itemlist:
		link_list.append("http://www.bestbuy.com"+item.group(1).strip())

def writeFile():
	try:
		for i in range(len(reviewtext_list)):
			global review_num
			fw.write('bestbuy.com'+'\t'+reviewtext_list[i].encode('utf-8')+'\t'+rating_list[i]+'\t'+date_list[i]+'\n') 
			review_num+=1
		del reviewtext_list[:]
		del rating_list[:]
		del date_list[:]
	except Exception, e:
		print e

def parsePage(html):
	global review_num
	getReview(html)
	getRating(html)
	getDate(html)
	#write to file
	writeFile()
	print 'page',page,'done'



#main url of the item
url='http://www.bestbuy.com/site/searchpage.jsp?st=samsung+tv&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=15&sp=&qp=&list=n&iht=y&usc=All+Categories&ks=960&keys=keys'

#open the browser and visit the url
driver = webdriver.Chrome('./chromedriver')
driver.get(url)

#sleep for 2 seconds
time.sleep(2)

#get the page url list
getItemList(driver.page_source)

for link in link_list:
	page = 1
	print "Scraping:\n"+link
	driver.get(link)
	#find the 'Ratings and Reviews' button based on its css path
	button=driver.find_element_by_css_selector('#ui-id-3')
	button.click() #click on the button
	time.sleep(2) #sleep
	#parse the first page
	if review_num >=10:
		break
	parsePage(driver.page_source)
	
	

	page=2
	while review_num<10:
	    #get the css path of the 'next' button
	    cssPath='#BVRRDisplayContentFooterID > div > span.BVRRPageLink.BVRRNextPage > a'
	    
	    try:
	        button=driver.find_element_by_css_selector(cssPath)
	    except:
	        error_type, error_obj, error_info = sys.exc_info()
	        print 'STOPPING - COULD NOT FIND THE LINK TO PAGE: ', page
	        print error_type, 'Line:', error_info.tb_lineno
	        break

	    #click the button to go the next page, then sleep    
	    button.click()
	    time.sleep(2)
	    
	    #parse the page
	    parsePage(driver.page_source)
	    
	    page+=1
	    
fw.close()


"""
Created on Fri Oct  2 22:53:12 2015
Walmart
"""
#import the two libraries we will be using in this script
import urllib2,re,sys


#make a new browser, this will download pages from the web for us. This is done by calling the 
#build_opener() method from the urllib2 library
browser=urllib2.build_opener()

#desguise the browser, so that websites think it is an actual browser running on a computer
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

 
#number of pages you want to retrieve (remember: 20 reviews per page)
pagesToGet=60

#create a new file, which we will use to store the links to the freelancers. The 'w' parameter signifies that the file will be used for writing.
fileWriter=open('walmartreviews.txt','w') #write


#for every number in the range from 1 to pageNum+1  
for page in range(1,pagesToGet+1):
    
    print 'processing page :', page
    
    #make the full page url by appending the page num to the end of the standard prefix
    #we use the str() function because we cannot concatenate strings with numbers. We need
    #to convert the number to a string first.
    url='https://www.walmart.com/reviews/product/25059351?limit=20&page='+str(page)+'&sort=helpful'

    try:
        #use the browser to get the url.
        response=browser.open(url)    
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print 'ERROR FOR LINK:',url
        print error_type, 'Line:', error_info.tb_lineno
        continue
        
    #read the response in html format. This is essentially a long piece of text
    myHTML=response.read()
    reviewPage=re.finditer('data-content-id=(.*?)<span class=customer-name-heavy>(.*?)review-media-img',myHTML)
   
    for reviews in reviewPage:
        text = re.search('data-max-height=110>(.*?)</p>',reviews.group(2)).group(1).replace('&#39;',"'").replace('\n',' ').replace('&amp;','&').replace('&#34;','"')
        rating = re.search('<div class="stars customer-stars">(.*?)visuallyhidden>(.*?) stars</span> <span class="customer-review-date hide-content-m">',reviews.group(1)).group(2)
        date = re.search('<span class="customer-review-date hide-content-m">(.*?)</span>',reviews.group(1)).group(1)   
        fileWriter.write( 'walmart.com' + '\t' +text + '\t' + rating + '\t' + date + '\n') 
    #count lines in txt, load at least 1000 reviews 
    count = len(open("walmartreviews.txt",'rU').readlines())
    if count > 1050: break
#close the file. File that are opened must always be closed to make sure everything is actually written and finalized.
fileWriter.close()

"""
Created on Thu Oct 01 21:40:46 2015
eBay
"""

import urllib2,re,sys,time
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

def combine_lines(text):
    lines = text.split('\n')
    newText = ''
    for line in lines:
        newText = newText + line
    return newText
    
browser = urllib2.build_opener()
browser.addheaders =[('User-agent', 'Mozilla/5.0')]

TV_Links=open('TvLinks.txt','w')


pagesToGet=100

for page in range(1,pagesToGet+1):
    print 'processing page :', page
    if page is 1:
        URL='http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=tv&rt=nc'
        try:
            response=browser.open(URL)    
        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            print 'ERROR FOR LINK:',URL
            print error_type, 'Line:', error_info.tb_lineno
            continue
        html=response.read()
        links=re.finditer('<h3 class="lvtitle"><a href="(.*?)"',html,re.S)
        for link in links:
            linkOfOneTv=link.group(1)
            TV_Links.write(linkOfOneTv+'\n')
    else:
        URL='http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=tv&_pgn='+str(page)+'&_skc=50&rt=nc'
        try:
            response=browser.open(URL)    
        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            print 'ERROR FOR LINK:',URL
            print error_type, 'Line:', error_info.tb_lineno
            continue
        html=response.read()
        links=re.finditer('<h3 class="lvtitle"><a href="(.*?)"',html,re.S)
        for link in links:
            linkOfOneTv=link.group(1)
            TV_Links.write(linkOfOneTv+'\n')
  
        
TV_Links.close()

fileReader=open('TVLinks.txt')
reviewsWriter=open('eBayreviews.txt','w')
count=0
for line in fileReader:
    MYURL=line.strip()
    try:
        response=browser.open(MYURL)    
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print 'ERROR FOR LINK:',MYURL
        print error_type, 'Line:', error_info.tb_lineno
        continue
    try:    
        Html=response.read()
    except httplib.IncompleteRead as e:
        Html = e.partial
        
    reviewMatches=re.finditer('class="ebay-review-section-l">(.*?)>.*?class="review-item-date">(.*?)</span>.*?class="review-item-content wrap-spaces">(.*?)</p>',Html,re.S)

    for match in reviewMatches:
        Rating=match.group(1)
        reviewRating=re.search('(\d.\d) out of 5 stars',Rating).group(1)
        reviewDate=match.group(2)
        text=match.group(3)
        reviewText=combine_lines(text)
        count+=1
        del match
        reviewsWriter.write('ebay.com'+'\t'+reviewText+'\t'+reviewRating+'\t'+reviewDate+'\n')
        print 'processing review:',count
    if count > 1000:
        break
print 'count of reviews=',count   
reviewsWriter.close()



BB = open('Bestbuyresult.txt')
A = open('Amazonreviews.txt')
eB = open('eBayreviews.txt')
WM = open('walmartreviews.txt')
out_file = open('reviews.txt', 'w')


for line in A:
    out_file.write(line)
for line in BB:
    out_file.write(line)
for line in WM:
    out_file.write(line)
for line in eB:
    out_file.write(line)
    

BB.close()
A.close()
eB.close()
WM.close()
out_file.close()

'''


Flowings are further transfermation:


from dateutil.parser import parse

raw_data = open('reviews.txt')
new_data = open('new.txt', 'w')
posLex=loadLexicon('positive-words.txt')


word_freq=dict()
posList=[]

for line in raw_data: # for every line in the input

    line=line.strip() 
    
    columns=line.split('\t') # split according to the delimeter
  
    website=columns[0] # get the user
    reviews=columns[1] # get the day   
    rating=columns[2]    #get the post
    date=columns[3]
    words=reviews.split(' ')
    #words=post.split(' ')#split the post on the space to get a list of the words
    for word in words: # for each word in the post
        if word in word_freq:# the word has been seen before, add +1 to its count.
            word_freq[word]=word_freq[word]+1
        else:
            word_freq[word]=1
    
    for d in date:
        d = parse(date)
    
    
    new_data.write(website+'\t'+reviews+'\t'+rating.replace(' out of 5 stars','')+'\t'+d.strftime('%d/%m/%Y')+'\n')


raw_data.close()
new_data.close()
'''


