"""
Created on Monday 04 January 2021  

Group 2 - Recherche de nouvelles sources
Crawler par site

@author : Maël Lesavourey
"""

# LIBRARIES

from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm


# QUERY INSIDE SITE

def get_query_src_page(pages: int, keywords: list, source_url: str, 
                       search_url: str, url_attr: str = None, 
                       separator: str = '+') -> list:
    """Documentation

    Get the source code of the pages resulting a research of a keyword.

    Parameters:
        pages: The number of pages you want to retrieve.
        keywords: List of keywords used in the research.
        source_url: URL of the website.
        search_url: The part of URL before keywords (ex: search?q=).
        url_attr: PHP attributes that may be after the keyword.
        separator: The separator between keywords in URL.

    Out:
        page_list: List containing the source code of each page of the research
    """
    # Initialize webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome('chromedriver', options=chrome_options)

    # Base url
    base = source_url + search_url
    if url_attr is None:
        for kw in keywords:
            base += kw + separator
        base = base[:-len(separator)]
    else:
        for kw in keywords:
            base += kw + separator
        base = base[:-len(separator)]
        base += '/' + url_attr
    page_list = []
    """ 
    This loop may be used when you will treat page switching.
    Note that you will need a condition to distinguish 2 cases : 
        -the switch is managed by URL.
        -the switch is managed dynamically.
        
    for i in tqdm(range(pages)):
        k = i + 1
        # Simulate a webdriver instance and get the source page 
        wd.get(base + '&page=' + str(k))
        # Transform it with the BS' html parser
        soup = BeautifulSoup(wd.page_source)
        page_list.append(soup)"""
        
    # Simulate a webdriver instance and get the source page 
    wd.get(base)
    # Transform it with the BS' html parser
    soup = BeautifulSoup(wd.page_source)
    page_list.append(soup)
    
    return page_list



def get_art_url(page_list: list, source_url: str, tag: str, 
                attr_key: str = None, attr_value: str = None) -> list:
    """Documentation:

    Get the article's urls.
   
    Parameters:
        page_list: list of pages' source code.
        source_url: URL of source website.
        tag:  tag of the closest identifiable tag.
        attr_key: attribute key of the closest identifiable tag.
        attr_value: attribute value of the closest identifiable tag.
        
    Out:
        url_list: list of the urls.
    """
    
    attr: dict = {attr_key : attr_value}
    url_list = []
    for page in tqdm(page_list):
        tag_list = page.find_all(tag, attr)
    
        if tag == 'a':
            for article in tag_list:
                url_list.append(article['href'])
        else :
            for article in tag_list:
                hyperlink = article.find('a') # <a> tags contain the urls
                url_list.append(hyperlink['href'])
    # Delete potential duplicates
    url_list = list(set(url_list))
    
    # Delete specific urls
    # Note that these conditions could be improven so the algorithm can delete
    # more or more specific unwanted url
    url_list_clean: list = []
    for i in range(len(url_list)):
        if ('http' not in url_list[i]):
            if (url_list[i] != '#'):
                url_list_clean.append(source_url + url_list[i])
        else :
            if source_url in url_list[i]:
                url_list_clean.append(url_list[i])
    return url_list_clean