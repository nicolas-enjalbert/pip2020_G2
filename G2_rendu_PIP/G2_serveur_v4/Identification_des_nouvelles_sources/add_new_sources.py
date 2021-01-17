import pandas as pd
import json


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