#!/usr/local/bin/python3.5.1
import urllib
import sys
import os
import future
import builtins
import bs4
import pdfcrowd
from bs4 import BeautifulSoup, SoupStrainer
from future.standard_library import install_aliases
install_aliases()
from urllib.request import urlopen, Request
from builtins import input

# Saving HTML page as PDF

def save_as_pdf(s,title,acc_name,acc_key):
    try:
        client = pdfcrowd.Client(str(acc_name), str(acc_key))
        output_file = open(title+'.pdf', 'wb')
        client.convertHtml(s, output_file)
        output_file.close()
        print("Saved file "+title+".pdf !")
    except pdfcrowd.Error:
        print('Failed')

########----- Modifying the CSS of the page for better user experience ------#######

def modify(url,acc_name,acc_key):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,"html.parser")
    b=soup.find("div", { "id" : "primary"})
    b['style']='float: none; margin: 0 auto !important; width: 90% !important;'
    a=soup.find("div", { "id" : "secondary"})
    a['style']='display: none'

    c=soup.findAll("h1")
    for c1 in c:
        c1['style']='line-height:1.2'
    d=soup.findAll("h2")
    for d1 in d:
            d1['style']='line-height:1.2'
    e=soup.findAll("h3")
    for e1 in e:
        e1['style']='line-height:1.2'

    f=soup.find("body")
    f['style']='line-height:1.6 !important; font-size:18px !important; color:#444 !important;padding:0 10px !important;'
    g=soup.find("header", {"id":"masthead"})
    g['style']='display:none'
    h=soup.find("aside", {"class":"widget_tag_cloud"})
    h['style']='display:none'
    ad=soup.find("ins", {"class":"adsbygoogle"})
    ad['style']='display:none'

    nav=soup.find("nav", {"class":"nav-single"})
    nav['style']='display:none'
    widget=soup.findAll("div", {"class":"textwidget"})
    for wid in widget:
        wid['style']='display:none'
    plugin=soup.find("div", {"class":"plugins"})
    plugin['style']='display:none'
    center=soup.find("center")
    center['style']='display:none'
    footer=soup.find("footer")
    footer['style']='display:none'
    textwidget=soup.find("aside", {"id":"text-14"})
    textwidget['style']='display:none'
    save_as_pdf(soup.prettify(),soup.title.contents[0],acc_name,acc_key)

########----- End of CSS ------#######

print("\n\n\t\t\t\t\tWelcome!\n\nDownload all  articles of GeeksforGeeks, topic wise, within a minute\n ")
acc_name = input("Please create a free HTML to PDF API account on PDFcrowd first, link: https://pdfcrowd.com/user/sign_up/?pid=default\n\nAfter that please go to your account details ( https://pdfcrowd.com/user/account/ ) and input your Username:\n\n")
acc_key = input("\nNow enter your API key:\n\n")
type = input("\nWant to download a particular: \n\n1. Category, or\n2. Tag\n\n")
topic = input("\nEnter the name of the topic or company, as per the url on GeeksforGeeks, eg- amazon, tree, sap-labs etc: \n\n")

choice=""
if type=='1':
    choice="category"
if type=='2':
    choice="tag"

if not os.path.exists(str(topic).title()):
    os.makedirs(str(topic).title())
    print("\nCreated folder "+str(topic).title())
    
os.chdir(str(topic).title())
i=1
page1 = urllib.request.Request("http://www.geeksforgeeks.org/"+choice+"/"+topic+"/page/"+str(i))
try:
    page = urllib.request.urlopen(page1).read()
    while page:
        try:
            i=i+1
            page = urllib.request.urlopen("http://www.geeksforgeeks.org/"+choice+"/"+topic+"/page/"+str(i)).read()
            soup1 = BeautifulSoup(page,"html.parser")
            #selector = soup1.find_all("article", {"class":"type-post"})
            for link in soup1.find_all("article", {"class":"type-post"}):
                nest=soup1.select('article.type-post h2.entry-title a')
                for nest1 in nest:
                    modify(nest1.attrs["href"],acc_name,acc_key)
        except urllib.error.HTTPError as e: sys.exit(1)
except urllib.error.HTTPError as e:
    print('The category/tag couldn\'t the topic/company, please check the page again and enter the correct data!')
    sys.exit(1)


print("Done! Thank you, hope you liked it. Incase you did, do not forget to star it on ")


# GeeksforGeeks_Downloader
