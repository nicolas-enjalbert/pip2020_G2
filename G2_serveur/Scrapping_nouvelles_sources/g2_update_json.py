"""
Created on Thursday 14 January 2021  

Group 2 - Recherche de nouvelles sources  
Update tags repository for crawler

@author : Maël Lesavourey
"""

import pandas as pd

def add_line_json(link: str, infos: list):
    """Documentation
    Allows to add a line into the sources
    """
    df: pd.DataFrame = pd.read_json(link)
    df.loc[len(df)] = infos
    df.to_json(link)