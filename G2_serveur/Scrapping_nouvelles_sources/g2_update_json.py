"""
Created on Thursday 14 January 2021  

Group 2 - Recherche de nouvelles sources  
Update tags repository for crawler

@author : Maël Lesavourey
"""

import pandas as pd

def add_line_json(path: str, info: list):
    """Documentation
    
    Allows to add a line into the sources
    
    Parameters: 
        path: String of the path to json file
        info: List of information to be add on json file
    """
    df: pd.DataFrame = pd.read_json(path)
    df.loc[len(df)] = info
    df.to_json(path)