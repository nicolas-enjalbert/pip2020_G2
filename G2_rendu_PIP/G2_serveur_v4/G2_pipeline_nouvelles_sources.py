# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:42:23 2021
Group 2
@authors : N.E.C,  A.D
"""

# Importing files
from Identification_des_nouvelles_sources.g2_Launch_Crawler_v6 import *
from Identification_des_nouvelles_sources.Parameters import *
from Identification_des_nouvelles_sources.g2_Create_Word_Combination_v6 import *
from Identification_des_nouvelles_sources.g2_Remove_Sites_v6 import *
from Identification_des_nouvelles_sources.g2_Launch_Pertinence_v6 import *
from Identification_des_nouvelles_sources.add_new_sources_v6 import *
import pandas as pd

def NewSources():
    ########## Folders ##########
    
    # General directory
    #☺global path_general
    path_general = ''
    
    # Directory to store crawled URLs
    #global path_links_crawler
    path_links_crawler = path_general + 'Données/'
    
    # Directory to store partial backups
    #global path_backup
    path_backup = path_general + 'Données/'
    
    # Directory to load files
    #global path_files
    path_files = path_general + 'Données/'
    
    # Directory to store crawled URLs
    path_links_crawler = path_general + 'Données/'
    
    #Parameters
    path_param = path_general + 'Identification_des_nouvelles_sources/'
    
    
    ########## Parameters ##########
    
    # API Key (created on Scraper API)
    API_KEY = open(path_param+'API_key.txt', 'r').read()
    
    # Last crawling date
    p_date = open(path_param+'date_last_crawling.txt', 'r').read()
    
    
    ########## Launch files ##########
    
    # Create equations
    listCouple = Create_Word_Combination(path_files)
    
    
    # Test on a few couples
    p_listCouple = listCouple
    
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
    #df_score.to_csv('pertinence.csv')
    
    Add_New_Sources(df_score, 0.9, path_links_crawler, path_files)
    
    
    


NewSources()


































