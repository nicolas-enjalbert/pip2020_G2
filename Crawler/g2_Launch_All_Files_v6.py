# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:42:23 2021
Group 2
@authors : A.D
"""

# Change working directory if it doesn't work
# cd C:\Users\degau\Desktop\Documents Audrey\Travail\M2 SID\Projet Interpromo

########## Importing files ##########

from Parameters import *
from g2_Create_Word_Combination_v6 import *
from g2_Launch_Crawler_v6 import *
from g2_Remove_Sites_v6 import *
from g2_Launch_Pertinence_v6 import *
from add_new_sources_v6 import *


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


# Test on some couples
p_listCouple = listCouple[0:2]

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

# Adding the new sources to the old ones
Add_New_Sources(df_score, 0.6, path_links_crawler, path_files)


















