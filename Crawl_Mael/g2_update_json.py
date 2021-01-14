"""
Created on Thursday 14 January 2021  

Group 2 - Recherche de nouvelles sources  
Update tags repository for crawler

@author : Maël Lesavourey
"""

import pandas as pd

def update_json(link: str, infos: list):
    df = pd.read_json(link)
    df.loc[len(df)] = infos
    df.to_json(link)