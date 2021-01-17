# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:02:33 2021
Group 2
@authors : A.D, C.P-M
"""

########## Module import ##########

import pandas as pd


########## Functions ##########

def remove_sites_lists(df, list_G1: list, list_uninteresting: list):
    """Documentation

    Remove the sites we don't want

    Parameters :
        df : the dataFrame containing the Google results crawled
        list_G1 : the list of the sites the G1 scrapped
        list_uninteresting : a list of non-pertinent sites like linkedin,
                             facebook, etc

    Out :
        df_new : the dataframe without the sites we don't want
    """

    # Concatenation of the 2 lists
    list_remove: list = list_G1+list_uninteresting
    list_url = []

    # Get the URLs we don't want
    for index, row in df.iterrows():
        if (any(site in row['URL'] for site in list_remove)):
            list_url.append(row['URL'])

    # Remove it from the dataframe
    df_new = df[~df['URL'].isin(list_url)]

    return df_new


def Remove_Sites(df_crawling, path_files, path_links_crawler):
    """Documentation

    Load the list of the sites the G1 scrapped and the list of the
    non-pertinent sites. Then remove this sites from the dataframe containing
    the URLs crawled on Google

    Parameters :
        df_crawling : the dataFrame containing the Google results crawled
        path_files : directory to load files
        path_links_crawler : directory to store crawled URLs

    Out :
        df_crawling_clean : the dataframe without the sites we don't want
    """
    
    
    # Openning the list of the sites the G1 scrapped
    list_G1 = pd.read_json(path_files+'Sites_g1.json')[0].tolist()
    list_G1_clean = list_G1 #[x for x in list_G1]

    # Openning the list of the non-pertinent sites
    list_uninteresting = pd.read_json(path_files+'Sites_uninteresting.json')[0].tolist()
    list_uninteresting_clean = list_uninteresting #[x for x in list_uninteresting]


    # Remove the sites we don't want
    df_crawling_clean = remove_sites_lists(df_crawling,
                                           list_G1_clean,
                                           list_uninteresting_clean)

    # Reset the index
    df_crawling_clean = df_crawling_clean.reset_index().drop(columns=['index'])

    # Storing the data in JSON format
    df_crawling_clean.to_json(path_links_crawler+'df_crawling_clean.json',
                              orient='index')

    return df_crawling_clean













