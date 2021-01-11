#prendre la liste des équations de recherches dans 'Données/liste_requete.json'
import pandas as pd

queries = pd.read_json('/home/sid2019-7/Documents/M2/PIP2021/G2_serveur/Données /liste_requetes.json')
print(queries)

#assembler les mots clefs 

#lire le fichier API_key.txt
import datetime
API_key = open("/home/sid2019-7/Documents/M2/PIP2021/G2_serveur/Identification_des_nouvelles_sources/API_key.txt", 'r').read()

string = datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")


dateCrawl = open("/home/sid2019-7/Documents/M2/PIP2021/G2_serveur/Identification_des_nouvelles_sources/google_crawling_derniere_date.txt", 'r').read()
dateCrawl = datetime.datetime.strptime(dateCrawl, '%Y/%m/%d - %H:%M:%S')


print(dateCrawl)






















#A la fin du crawler google
fichier = open("/home/sid2019-7/Documents/M2/PIP2021/G2_serveur/Identification_des_nouvelles_sources/google_crawling_derniere_date.txt", "w")
fichier.write(string)
fichier.close()