# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:36:09 2021
Group 2
@authors : A.D, C.P-M, Y.S
"""

########## Module import ##########

import re
import random
import json
import nltk
nltk.download('stopwords')


########## Functions ##########

def around_query(lexicon):
    """Documentation

    Removing stop words and adding the 'AROUND(2)' keyword between the compound
    words

    Parameters :
        lexicon : lexicon to process

    Out :
        liste : lexicon processed
    """

    liste = lexicon.copy()
    # Tokenize lexicon
    liste = [tokenize(i) for i in liste]
    # Remove stop words
    liste = [remove_stopwords(i) for i in liste]
    for i in range(len(liste)):
        if len(liste[i]) == 1:
            liste[i] = liste[i][0]
        else:
            texte = liste[i][0]
            for j in range(1, len(liste[i])):
                # Add the 'AROUND(2)' keyword if it is a compound word
                texte += ' AROUND(2) ' + liste[i][j]
            liste[i] = texte

    return liste


def remove_stopwords(tokenzed_list):
    """Documentation

    Removing stop words from a tokenized list of words

    Parameters :
        tokenzed_list : tokenized list of words

    Out :
        text : list without stopwords
    """

    stopwords = (tuple(nltk.corpus.stopwords.words('french')))
    text = [word for word in tokenzed_list if word not in stopwords]

    return text


def tokenize(text):
    """Documentation

    Tokenize the keywords of the lexicon

    Parameters :
        text : keyword or compound keyword to tokenize

    Out :
        tokens : tokenized keywords
    """

    tokens = re.split('\s|[\']', text)

    return tokens


def cartesien(liste1, liste2):
    """Documentation

    Makes the Cartesian product from 2 lists

    Parameters :
        liste1 : innovation lexicon
        liste2 : gestion lexicon

    Out :
        listeCouples : list of couples resulting from the Cartesian product
    """

    listeCouples = []
    for i in range(len(liste1)):
        for y in range(len(liste2)):
            listeCouples.append([liste1[i], liste2[y]])

    return listeCouples


########## Create Word Combination ##########

def Create_Word_Combination(path_files):
    """Documentation

    Create couples of keywords from the Innovation and Gestion lexicons

    Parameters :
        path_files : directory where the 2 lexicons are stocked

    Out :
        liste_couples : list of couples resulting from the combination of
                        innovation and gestion keywords
    """

    # Opening lexicons and turning them into lists
    with open(path_files+'Lexique_Gammes_Gestion.txt', encoding="utf-8") as img:
        gestion = img.readlines()
    with open(path_files+'Lexique_Innovation.txt', encoding="utf-8") as img:
        innovation = img.readlines()

    # Remove /n
    for i in range(len(gestion)):
        gestion[i] = gestion[i][:-1]
    for i in range(len(innovation)):
        innovation[i] = innovation[i][:-1]

    # Removing stop words and adding the 'AROUND(2)' keyword between the
    # compound words
    lexique_gestion_tokenize = around_query(gestion)
    lexique_innovation_tokenize = around_query(innovation)

    # Makes the Cartesian product from the 2 lexicons
    liste_couples = cartesien(lexique_innovation_tokenize,
                              lexique_gestion_tokenize)

    # Mix the list of couples
    random.shuffle(liste_couples)

    # Saving the results
    with open(path_files+'liste_couples_shuffle.json', 'w') as jsonfile:
        json.dump(liste_couples, jsonfile)

    return liste_couples
