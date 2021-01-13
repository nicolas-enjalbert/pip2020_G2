from Scrapping_nouvelles_sources.crawler_par_site import *
from Scrapping_nouvelles_sources.BigScraper import *
import pandas as pd

def dailyScrapping():
    #Import list of sources
    sources=pd.read_json('Données/sources.json',orient='records')
    
    
    #Ici faire une entrée avec le crawler par site
    urls = crawling(sources)
    
    
    
    
    


    BG = BigScraper()
    urls = pd.read_json('listTestArt.json')
    
    
    for url in urls.art_url[12:13]:
        print(url)
        row = BG.scrap(url)
    
    BG.df.to_json('scrapedData.json', orient='records')
    return BG.df

dailyScrapping()

