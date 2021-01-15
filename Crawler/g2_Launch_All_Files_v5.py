# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:42:23 2021

@author: degau
"""

########## Importing files ##########

from Parameters import *
from g2_Create_Word_Combination_v5 import *
from g2_Launch_Crawler_v5 import *
from g2_Remove_Sites_v5 import *
from g2_Launch_Pertinence_v5 import *


########## Folders ##########

# General directory
path_general = 'C:/Users/degau/Desktop/Documents Audrey/Travail/M2 SID/'

# Directory to store crawled URLs
path_links_crawler = path_general + 'Projet Interpromo/Test/'

# Directory to store partial backups
path_backup = path_general + 'Projet Interpromo/Test/'

# Directory to load files
path_files = path_general + 'Projet Interpromo/'


########## Parameters ##########

# API Key (created on Scraper API)
API_KEY = open(path_files+'API_key.txt', 'r').read()

# Last crawling date
p_date = open(path_files+'date_last_crawling.txt', 'r').read()


########## Launch files ##########

# Create equations
listCouple = Create_Word_Combination(path_files)


# Test on a few couples
p_listCouple = listCouple[0:274]

# Launch crawling
df_crawling = Launch_Crawler(p_listCouple,
                             API_KEY,
                             p_date,
                             p_length,
                             p_requestNumber,
                             p_nb_results,
                             path_general,
                             path_links_crawler,
                             path_backup,
                             path_files)



# Remove some websites
df_crawling_remove = Remove_Sites(df_crawling, path_files, path_links_crawler)


# Calculate pertinence
df_score = Launch_Pertinence(df_crawling_remove)
df_score

# Add new sources
def Add_New_Sources(seuil, df_score, path_links_crawler, path_files):
    
    list_new_sources = list(df_score[df_score['score_mean'] > seuil]['src_name'])
    
    with open(path_links_crawler+'list_new_sources.json', 'w') as jsonfile:
        json.dump(list_new_sources, jsonfile)
    
    
    old_sources = pd.read_json(path_files+'list_old_sources.json', orient ='records').values.tolist()
    old = [x[0] for x in old_sources]
    
    list_add = []
    for new in list_new_sources:
        if(new not in old):
            list_add.append(new)
    
    with open(path_files+'list_old_sources.json', 'w') as jsonfile:
        json.dump(old+list_add, jsonfile)



Add_New_Sources(0.6, df_score, path_links_crawler, path_files)


















