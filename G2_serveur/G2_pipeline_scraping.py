from Scrapping_nouvelles_sources.g2_crawl_by_site_v1 import *
from Scrapping_nouvelles_sources.BigScraper import *
import pandas as pd

def dailyScrapping():
    #Import list of sources
    sources = pd.read_json('Données/tags_crawl.json')
    keywords = #import
    
    #Ici faire une entrée avec le crawler par site
    list_url = []
    for i in sources.index:
        for kw in keywords:
            pages = get_query_src_page(pages=, keywords=kw, 
                                       source_url=sources['url_source'][i], 
                                       search_url=sources['url_search'][i], 
                                       url_attr=None, 
                                       separator=sources['separator'][i])
            list_url.append(
                    get_art_url(page_list=pages, 
                                source_url=sources['url_source'][i], 
                                tag=sources['tag_art'][i], 
                                attr_key=sources['attr_key'][i], 
                                attr_value=['attr_value'][i])
                    )
    
    
    
    


    BG = BigScraper()
    urls = pd.read_json('listTestArt.json')
    
    
    for url in urls.art_url[12:13]:
        print(url)
        row = BG.scrap(url)
    
    BG.df.to_json('scrapedData.json', orient='records')
    return BG.df

dailyScrapping()

