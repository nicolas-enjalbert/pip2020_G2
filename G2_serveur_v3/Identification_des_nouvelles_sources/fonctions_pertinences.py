import pandas as pd
import numpy as np
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()
import pickle
from nltk.corpus import stopwords
stop_words = set(stopwords.words('french'))
from nltk.stem import LancasterStemmer
from nltk.stem import SnowballStemmer


#### préparation des données ####
def prepareDF(df): 
    df['src_name'] = [site_name(url) for url in df.art_url]
    df["src_url"] = [get_base_url(url) for url in df.art_url]
    return df




def site_name(url: str) -> str :
    """Documentation

        Parameter:
            url: complete url of an article

        Out:
            base_url: name of a website

        """
    site = url.split("://")
    if site[0] == "https" or site[0] == "http":
        name_site = site[1]
    else:
        name_site = site[0]
    tab = name_site.split("/")
    name_site = tab[0]
    TLD = ["fr.","www.","www2.",".org",".fr",".eu",".net",".com"]
    for i in TLD:
        name_site = name_site.replace(i, "")
    return(name_site)

def get_base_url(url: str) -> str:
        """Documentation

        Parameter:
            url: complete url of an article

        Out:
            base_url: base url of a website

        """
        for val in re.finditer(r"(\w)+://[^/]+/", url):
            base_url = val.group(0)
        return base_url
    
    
#### Popularité ####
def countSite(df):
  return df.groupby('src_name').count().reset_index()

def popularite(df):
    """
    Parameters
    ----------
    df : DataFrame
        Contains : art_url, src_name, src_url.

    Returns
    -------
    DataFrame
        Contains : src_name, popularity score.

    """
    df1 = countSite(df)
    df1["popularity"] = [x/max(df1.art_url) for x in df1.art_url]
    df_final = df1[['src_name','popularity']]
    return df_final
    




#### Valeur de requête dans titre ou résumé ####
def common_query_words(df) :    
  df_relevance = pd.DataFrame(columns=['nb_row','score']).set_index('nb_row') #creation of a df allowing to have the score for each line,
  for j in range (len(df)): # for each line of the df,
    innov : int = 0 #initialization of a variable to count the number of words in the innovation lexicon 
    gest : int = 0 #...the same for the management lexicon
    separator_or : list = list(df['query'][j].split(' or ')) #we store all pairs of the request in a separator_or list 
    relevance_listing : list = [] #list to store the relevance scores for each of the couples
    list_find : list = [] #list to store words in common for each line,
    for k in range (len(separator_or)): #for each of these couples,
      nb_present : int = 0 #count the number of words in common
      separator_and : list = list(separator_or[k].split(' and ')) #we store all the words of the couple of the query in a separator_and list 
      for i in range (len(separator_and)): #for all the words in the query,
        if (df['title'][j].find(separator_and[i]) != -1) : #we look for it in the title, and if it's there... 
          if (i == 0): #if it's the first member of the couple, we've found a word of innovation 
            innov += 1
          else : #If not, a word of management 
            gest += 1
          nb_present = nb_present + 1 #increments the number of words in the query found.  
          list_find.append(separator_and[i]+";")
        if (df['resume'][j].find(separator_and[i]) != -1) : #then we look for it in the summary, and if it's there... 
          if (i == 0):
            innov += 1
          else :
            gest += 1
          nb_present += 1
          list_find.append(separator_and[i]+";") #... we put it in a list
          list_find = list(set(list_find))
      relevance_query : float = (nb_present / len(separator_and))*100 #we calculate the relevance score nb of words found / nb of total words in the query
      relevance_listing.append(relevance_query)
      str = ' '.join(list_find) #...
    df['common_words'][j]=str[:-1] #...we add the words found in the df
    df_relevance = df_relevance.append({'nb_row': j}, ignore_index=True)
    df_relevance['score'][j] = max(relevance_listing) #for each line, we take the best relevance of a couple,
    nb = df_relevance['score'][j]
    #and we categorize according to the score obtained :
    if (nb>=100) : #all the words of at least one couple are found,
      df['cat_pertinence'][j] = 'I&G'
    else :
      if (innov >= 1 and gest >= 1) : #words of innovation and gestion are found but not in the same couple,
        df['cat_pertinence'][j] = 'I&G but not from the same couple'
      elif (innov >= 1 and gest == 0) : #at least one word of innovation is found, but no gestion,
        df['cat_pertinence'][j] = 'I'
      elif (innov == 0 and gest >= 1): #at least one word of management is found but no innovation, 
        df['cat_pertinence'][j] = 'G'
      else :
        df['cat_pertinence'][j] = 'None' #no word is found 
  return(df)