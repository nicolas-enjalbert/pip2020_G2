
# -*- coding: utf-8 -*-
"""

#**STATISTICAL PART**

Created on Monday 04 January 2021  

**Group 2 - Identification of new sources**  

@authors : C.P.M, Y.S., S.B, A.D.

##**1/ Import of library**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
from pandas import DataFrame
import re
import nltk
import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import json
import scrapy


"""##**3/ Some statistics on the names of sites ...**

1 - Preparation of data
"""

# Step 1 : get the domain (site name) of the site thanks to the url of the article  

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
        base_url = ''
        for val in re.finditer(r"(\w)+://[^/]+/", url):
            base_url = val.group(0)
        return base_url


def prepareDF(df : pd.DataFrame): 
    """ Documentation

    Get the name and the URL of a website from the URL of an article

    Parameters :
        df : dataframe containing the results crawled without the sites we 
             don't want
    Out :
        df : dataframe containing 2 more columns (name and URL of the websites)
    """

    df['src_name'] = [site_name(url) for url in df.art_url]
    df["src_url"] = [get_base_url(url) for url in df.art_url]
    return df

# Step 2 : put all the names of the sites in a list ...

# Step 3 : ... or in a dataframe, as needed

#df_sites = DataFrame(list_sites,columns=['src_name'])


"""## **4/ Relevance score :**"""

#### Popularité ####
def countSite(df : pd.DataFrame):
  # Count the number of URLs crawled per site
  return df.groupby('src_name').count().reset_index()

def popularite(df : pd.DataFrame):
    """
    Calcule the popularity score per site

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
    df1["popularity"] = [x/np.max(df1.art_url) for x in df1.art_url]
    df_final = df1[['src_name','popularity']]
    return df_final


"""**2 -** Estimation of the relevance by taking the **words in common between those of the query, and those present in the title and in the Google summary** of the article."""

# Step 1 : Create the cleanup to get the root, remove punctuation and empty words

def cleandesc(desc : str):
    """ Documentation

    Removing stop words and stemming words

    Parameters :
        desc : string to process
    Out :
        sent : string processed
    """

    stop_words = set(stopwords.words('french'))
    sent = desc
    sent = "".join([x.lower() if x.isalpha()  else " " for x in sent])
    Porter = SnowballStemmer('french')
    sent = " ".join([Porter.stem(x) if x.lower() not in stop_words  else "" for x in sent.split()])
    sent = " ".join(sent.split())
    return sent


# Step 2 : Apply the cleaning function is applied 
def transform_data (df : pd.DataFrame):
  """ Documentation

    Remove stop words and apply stemming to titles, resumes and queries

    Parameters :
        df : dataframe processed
    Out :
        df : dataframe with clean and stemming titles, resumes and queries
  """

  start_time = time.time()
  df['title'] = [cleandesc(x.title) for x in df.itertuples()]
  df['resume'] = [cleandesc(x.resume) for x in df.itertuples()]
  df['query'] = [cleandesc(x.query) for x in df.itertuples()]
  end_time = time.time()
  print("total time : {} mn".format((end_time-start_time)/60))
  return (df)

# Step 3 : to do the function that will determine the relevance of the article according to the request 


def common_query_words(df : pd.DataFrame) :
  """ Documentation

    Calculate the relevance of the queries

    Parameters :
        df : dataframe processed
    Out :
        df : dataframe containing relevance score and categorie
  """

  df = transform_data(df)
  df['cat_pertinence'] = ''
  df['common_words'] = ''
  df['relevance_query']=0.00
  relevance_query : list = [] #list that will store the relevance score,
  #pertinence_j = [] #list that will store the number of the line concerned
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
          list_find.append(separator_and[i] +";") #... we put it in a list
          list_find = list(set(list_find))
      relevance_query : float = (nb_present / len(separator_and))*100 #we calculate the relevance score nb of words found / nb of total words in the query
      relevance_listing.append(relevance_query)
      str = ' '.join(list_find) #...
    df['common_words'][j]=str[:-1] #...we add the words found in the df
    df_relevance = df_relevance.append({'nb_row': j}, ignore_index=True)
    df_relevance['score'][j] = max(relevance_listing) #for each line, we take the best relevance of a couple,
    df['relevance_query'][j] = df_relevance['score'][j]
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

def result_score_def (df : pd.DataFrame):
  """ Documentation

    Calculate the relevance of a query per site

    Parameters :
        df : dataframe processed
    Out :
        df_result_score : dataframe containing the relevance of a query per
        site
  """

  df_relevance_query = common_query_words(df) # record our relevance scores obtained using common words
  df_relevance_query['src_name'] = ''
  for i in range (len(df_relevance_query)) :
    df_relevance_query['src_name'][i] = site_name(df_relevance_query['art_url'][i]) # add the name of the site in the dataframe according to the url 
  df_result_score = df_relevance_query.groupby('src_name')['relevance_query'].mean() # we make a groupby to have the average score according to the request per site 
  return (df_result_score) # return the new dataframe  

def relevance_query (df : pd.DataFrame) :
  """ Documentation

    Calculate the standardized relevance of a query per site

    Parameters :
        df : dataframe processed
    Out :
        df_result_score : dataframe containing the relevance of a query per
        site
  """

  df_result_score = result_score_def(df) # we record our relevance scores grouped by site, 
  df_result_score = df_result_score.reset_index()
  df_result_score['relevance_query'] = df_result_score['relevance_query']/(max(df_result_score['relevance_query'])) # they are divided by the maximum to get a relevance score between 0 and 1,
  return (df_result_score)

"""**3 -** Estimation of relevance by the **position of the article in the crawl**"""

def score_rank(df : pd.DataFrame) :
  """ Documentation

    Calculate the score rank per site based on the position of the item in the
    crawl 

    Parameters :
        df : dataframe processed
    Out :
        df_result_rank : dataframe containing the score rank per site
  """

  for i in range(df.shape[0]):
    df['score_rank'] = 1/((df['position']/df[df['query'] == df['query'].iloc[i]].shape[0])+1) # the rank score is calculated based on the position of the item in the crawl 
    df_result_rank = df.groupby('src_name')['score_rank'].mean() # we do a groupby to get the average of this score per site,
    return (df_result_rank)

def fusion_2(df : pd.DataFrame) :
  """ Documentation

    Calculate the relevance for each site crawled

    Parameters :
        df : dataframe containing the results crawled without the sites we 
             don't want
    Out :
        fusion_result : dataframe containing the score for each site crawled
  """

  df_prepare = prepareDF(df)
  fusion = pd.merge(popularite(df_prepare), relevance_query(df_prepare), how="right", left_on="src_name", right_on="src_name") #the new relevance score is merged with those obtained previously, 
  df_result_rank = score_rank(df_prepare)
  df_result_rank = df_result_rank.reset_index()
  fusion_result = pd.merge(fusion, df_result_rank, how="right", left_on="src_name", right_on="src_name")
  fusion_result['score_mean'] = 0.0
  for i in range (len(fusion_result)):
    fusion_result['score_mean'][i] = fusion_result['popularity'][i]*0.2 + fusion_result['relevance_query'][i]*0.4 + fusion_result['score_rank'][i]*0.4 #These scores are weighted by coefficients applied after reflection and an average relevance score is calculated,
  return(fusion_result)


def Launch_Pertinence(df_crawling_remove):
    """ Documentation

    Calculate the relevance for each site crawled and sort the results

    Parameters :
        df_crawling_remove : dataframe containing the results crawled without
                             the sites we don't want
    Out :
        df_score : dataframe containing the score for each site crawled
    """

    # Renaming the columns
    data = df_crawling_remove.rename(columns={'URL': 'art_url',
                                              'Query': 'query',
                                              'Title': 'title',
                                              'Snippet': 'resume',
                                              'Rank': 'position'})
    # Calculate the relevance
    df_new = fusion_2(data)
    # Sorting the results
    df_score = df_new.sort_values(by=['score_mean'], ascending=False)

    return df_score
