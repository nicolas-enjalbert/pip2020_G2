# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:02:33 2021

@author: degau
"""

########## Module import ##########

import pandas as pd


def retirer_sites(df, list_G1 : list, list_uninteresting : list):
    """ Documentation
    Parameters:
        df : a dataFrame of articles' URL
        list_G1 : the list of the sites the G1 scrapped
        list_uninteresting : a list of non-pertinent sites like linkedin, facebook, etc
    Out :
        df_new : the df without the sites we don't want
    """
    
    list_remove : list = list_G1+list_uninteresting #concatenation of the 2 lists
    list_url=[]
    for index, row in df.iterrows():
        if (any(site in row['URL'] for site in list_remove)):
            list_url.append(row['URL'])
    df_new = df[~df['URL'].isin(list_url)]  

    return df_new 


def Remove_Sites(df_crawling, path_files, path_links_crawler):
    
    list_G1 = pd.read_json(path_files+'Sites_g1.json')[0].tolist()
    list_G1_clean = list_G1 #[x for x in list_G1]
    list_uninteresting = pd.read_json(
            path_files+'Sites_uninteresting.json')[0].tolist()
    list_uninteresting_clean = list_uninteresting #[x for x in list_uninteresting]
    
    #list_G1 = pd.read_json(path_files+'Sites_g1.json', orient='index').T.values.tolist()
    #list_G1_clean = [x[0] for x in list_G1]
    #list_uninteresting = pd.read_json(path_files+'Sites_uninteresting.json', orient='index').T.values.tolist()
    #list_uninteresting_clean = [x[0] for x in list_uninteresting]
    
    df_crawling_clean = retirer_sites(
            df_crawling, list_G1_clean, list_uninteresting_clean)
    df_crawling_clean = df_crawling_clean.reset_index().drop(columns=['index'])
    
    # Storing the data in JSON format
    df_crawling_clean.to_json(
            path_links_crawler+'df_crawling_clean.json', orient='index')
    
    return df_crawling_clean













