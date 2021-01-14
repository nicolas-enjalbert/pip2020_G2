# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:18:14 2021

Group 2
Scrapping with Google API

@author: Marianne Manson
"""

import time
import json
from urllib.parse import urlencode
from requests import get
from bs4 import BeautifulSoup

# API Key (created on Scraper API)
API_KEY = '2daa0fbbc103c5172e706fcbc5845747'

def create_google_url(url_site):
    """
    Create the url for the google search of the new ressources 
    posted by the website during the last 24 hours
    
    Parameters:
        url_site : string of the website url
    
    Out:
        google : url of the search
    
    """
    google = "https://www.google.com/search?hl=fr"
    #site
    google += "&q=site%3A" + url_site
    #last 24 hours
    google += "&as_qdr=d"
    return google

def get_api_url(url):
    """ 
    Creation of the URL that will allow the legal scraping of Google results (use of the API key). 
    This URL is equivalent to a Google search.

    Parameter :
        url : google URL created from the url website (create_google_url)
    
    Out :
        proxy_url : URLs built using the API
    """

    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'fr'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

def scraping(url):     
    """ 
    Scrapping with scraperapi of the different pages of the google search

    Parameter :
        url : URL built using the API
    
    Out :
        list_src : list of scrapping results for the different pages
    """
    time.sleep(60)
    response = get(url)
    source = response.text
    list_src = [source]
    dic = json.loads(source)
    next_page = dic['pagination']['nextPageUrl']
    if next_page is not None:
        list_src.extend(scraping(get_api_url(next_page)))
    return list_src

def get_links(result_scrap):
    """ 
    Extraction of the links from the scrapping results of the google search

    Parameter :
        result_scrap : list of scrapping results
    
    Out :
        list_links : URL list
    """
    list_links = []
    for page in result_scrap:
        dico = json.loads(page)
        result = dico['organic_results']
        for i in range(len(result)):
            list_links.append(result[i]['link'])
    return list_links

def sort_articles(url_list):
    """ 
    Keep article URLs in the url_list (may not work on every site)

    Parameter :
        url_list : URL list
    
    Out :
        list_links : list of articles URL
    """
    list_links = []
    for i in range(len(url_list)):
            url = url_list[i]
            req = get(url)
            html_soup = BeautifulSoup(req.text, 'html.parser')
            meta = html_soup.find('meta',{'property':'og:type'})
            if meta is not None:
                og_type = meta['content']
                if og_type == "article":
                    list_links.append(url)
    return list_links

# Website used for testing
url_site_test = "https://www.zdnet.fr"

url_search_test = create_google_url(url_site_test)

url_api_test = get_api_url(url_search_test)

result_test = scraping(url_api_test)

url_links_test = get_links(result_test)

url_articles_test = sort_articles(url_links_test)

print(url_links_test)