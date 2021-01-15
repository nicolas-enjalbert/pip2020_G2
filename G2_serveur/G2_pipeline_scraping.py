from Scrapping_nouvelles_sources.g2_crawl_by_site_v1 import *
from Scrapping_nouvelles_sources.BigScraper import *
import pandas as pd

def dailyScrapping():
    """Documentation:

    This function calls several function of the project to get URL of articles
    in a site and scrap them.
   
    Parameters:
        
    Out:
        
    """
    #Import list of sources
    sources: pd.DataFrame = pd.read_json('Données/tags_crawl.json')
    sources: pd.DataFrame = sources.replace({np.nan: None})
    
    keywords:  = #import a list of list of kw or dataframe
    
    #Crawl by site
    list_url: list(list) = []
    for i in sources.index:
        for kw in keywords:
            #Generate source code of webpage
            #pages is fix to 1 because we didn't manage to treat the page
            #switch during the project.
            pages: list = get_query_src_page(pages=1, keywords=kw, 
                                       source_url=sources['url_source'][i], 
                                       search_url=sources['url_search'][i], 
                                       url_attr=sources['url_attr'][i], 
                                       separator=sources['separator'][i])
            #Get URL of each article
            list_url.append(
                    get_art_url(page_list=pages, 
                                source_url=sources['url_source'][i], 
                                tag=sources['tag_art'][i], 
                                attr_key=sources['attr_key'][i], 
                                attr_value=['attr_value'][i])
                    )
    
    #Create a flat list from the list of list "list_url"
    list_url_flat: list = [url for sublist in list_url for url in sublist]
        

    BG = BigScraper()
    urls = pd.read_json('listTestArt.json')
    
    
    for url in urls.art_url[12:13]:
        print(url)
        row = BG.scrap(url)
    
    BG.df.to_json('scrapedData.json', orient='records')
    return BG.df

dailyScrapping()

