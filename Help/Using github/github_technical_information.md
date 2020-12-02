---
title: Manipulation technique pour Github
author: Nicolas Enjalbert Courrech 
Date:     November 8, 2020 
---


# Manipulation technique pour Github: 

## Aller dans une branche : 

Dans le terminal : `git checkout yourBranch`

Dans Github : Dans le coin haut-gauche, choisir la branche yourBranch 

## Ajouter un dossier  

Dans le terminal : créer un dossier dans son local et faire un pull/add/comint/push vers le dépot github (cf. ) 

Dans github : créer un dossier dans son local -> aller dans l'onglet Code -> en haut à droite "add files" -> "Upload files" -> glisser le dossier depuis son gestionnaire de fichier local. 


## Utiliser le terminal pour le github

Si Git n'est pas installé, installez le. 

### Cloner un dépôt 
Se mettre dans le dossier visé avec le terminal (cd) puis faire la commande : 
    `git clone https://github.com/nicolas-enjalbert/DefisIA2021.git`
    
Le dossier DefisI12021 est créé. Se placer dedans pour utiliser les commandes Git `cd DefisIA2021`
Se munir de son pseudo et mot de passe git. 

### Se placer dans une branche

    `git checkout yourBranch`
Faire des modifications dans les fichiers locaux, créer des dossiers ou documents. 

### Envoyer les nouvelles informations au serveur github

Faire un pull 
`git pull`

Ajouter les informations 

    `git add - A`
    `git commit -m "Faire un message expliquant les modifications"`

Dans le message noté l'issue résolue par son numéro

Envoyer les informations 
    `git push`

  

