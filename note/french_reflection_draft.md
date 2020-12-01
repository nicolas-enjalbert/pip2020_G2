# Brouillon de réflexion 

## Indication sur le pp 

#### Objectifs 
 Identifier de nouvelles sources de donées contenant des articles pertinents pour le client et scrapper ces articles pertinents. 

   Difficulté : implémentation d'un scrapper générique
   
### Délivrables:   
  1. Données documentées
  2. Scripts de collecte commentés
  3. Notebook détaillé sur la création de modèles et la découverte de faisceaux de preuves pour établir la priorisation
  

## Réflexion personnelle
 

Le but du projet est d'identifier et scrapper les données du web sur de la veille technologique. Biensur je ne sais pas faire ça. 

Il faut identifier les bonnes sources de document. Une source correspond à un corpus de document pertinent. 

Une source potentielle contient plusieurs documents. 
Si cette source contient plusieurs documents pertinant alors elle est pertinente ? 


Première approche couteuse:  
  * créer un corpus pertinent de document : faire une requête type "moteur de recherche" sur l'ensemble des corpus (source).  
  * récuperer les sources et l'ensemble des documents de ces sources à partir du resultat de requête  
  * analyser l'ensemble des documents des sources et voir s'ils sont pertinents.  
  * Juger (avec une métrique) si la source est pertinente.  
    
Difficulté : comment juger la pertinence ?  
  1. Utiliser un modèle pré-entrainer (fonce Jérèm') 
  2. _Je ne sais pas et ca sera ça qu'il faudra que je fasse mdrrr_ 
  
  Comment selectionner les documents pertinents sur tout le web (multi source) ? 
  
  

## Moyen de scrapper et voir ce qu'on a sur internet

Les pages internet sont structurées et balisées donc on peut cibler les informations sont à un certains endroit. Pour des articles nous pouvons penser que le texte est dans les balises <p> dans le <body>. 
Mais qu'en est il des metadonnées ? il va falloir aller les chercher dans une autre balise. 
Issue : Comment faire en sorte que le modèle récupère toujours les bonnes informations ? 
Prépare toi à ce que ça ne soit pas parfait. Essaye de te donner un seuil par exemple il est concluant s'il récupère au moins 80% des bonnes informations au bon endroit.
=> difficultés de généralisation

The query parameters

_Beautiful Soup_ pas mal pour récuperer des informations sur un code HTML

  
  
# Retour de la séance de préparation du 25/11/20  

Le but du groupe est de trouver le plus de nouvelles sources possibles. Il faut donc avoir un rappel fort (nous avons le plus de vrai sources pertinentes dans notre collecte). On va donc ratisser large. 

Une des premières missions est de trouver un lexique sur l'INNOVATION. 
Il va falloir faire l'identification de ces sources => avoir une liste de sources. 
Récupérer les mots clefs qui ont permis de faire cette identification (/!\ car nécessaire pour Jérèm)

Les documents sont uniquement en français comme les mots clefs. Nous allons nous fixer aussi à des documents en francais 

Nous n'allons pas nous préoccupé dans un premier temps du dédoublenage  
Pour avoir la pertinence des sites web nous allons nous contenté dans un premier temps d'avoir des mots clefs de la thématique et de l'innovation (liste à finir de définir) 
Voir des thésaurus pour avoir d'autre mots clefs 

Voir pour faire un lancement automatique tous les x temps.  

granularité assez fine pour bien voi l'évaluation ? 



# Libraries et méthodes préselectionnées

https://makina-corpus.com/blog/metier/2018/seo-scraping-machine-learning-comprendre-le-fonctionnement-dun-moteur-de-recherche  

Faire un crawler pour selectionner les pages:  
  * _scrapy_ en python pour aller de page en page  
  * voir le ranking de google en page rank 



