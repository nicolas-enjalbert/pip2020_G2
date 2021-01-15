# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:42:23 2021

@author: degau
"""

########## Importing files ##########

from Parameters import *
from g2_Create_Word_Combination_v4 import *
from g2_Launch_Crawler_v4 import *
from g2_Remove_Sites_v4 import *


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


print(len(df_crawling))


# Remove some websites
df_crawling_remove = Remove_Sites(df_crawling, path_files, path_links_crawler)
print(len(df_crawling_remove))






















