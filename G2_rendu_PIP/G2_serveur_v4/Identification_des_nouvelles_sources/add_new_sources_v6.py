########## Module import ##########

import pandas as pd
import json


########## Function ##########

# Adding new sources
def Add_New_Sources(df_score: pd.DataFrame, threshold: list, 
                    path_links_crawler: str, path_files: str):
    """ Documentation

    Keep the most relevant sites from a threshold and compares them to the list
    of old sites. Then adding the new sites to the list of old ones

    Parameters :
        df_score : dataFrame containing the scores of the new sources
        threshold : threshold from which we consider a new source as relevant
        path_links_crawler : directory to store crawled URLs
        path_files : directory to load files
    """

    # Keep the most relevant sites from a threshold
    list_new_sources = \
    list(df_score[df_score['score_mean'] > threshold]['src_name'])

    # Save the most relevant sites
    with open(path_links_crawler+'list_new_sources.json', 'w') as jsonfile:
        json.dump(list_new_sources, jsonfile)

    # Open the list of old sources
    old_sources = pd.read_json(path_files+'list_old_sources.json',
                               orient='records').values.tolist()
    old = [x[0] for x in old_sources]

    # Compare the 2 lists
    list_add = []
    for new in list_new_sources:
        if(new not in old):
            list_add.append(new)

    # Add the new sources to the old ones
    with open(path_files+'list_old_sources.json', 'w') as jsonfile:
        json.dump(old+list_add, jsonfile)
