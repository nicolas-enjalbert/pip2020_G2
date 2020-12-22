---
title: Manipulation technique pour Github
author: Nicolas Enjalbert Courrech 
Date:     November 8, 2020 
---

Ce fichier est une aide mémoire, tutoriel pour l'utilisation de Github et ses interfaces possibles : GitKraken et le terminal de votre ordinateur.

# Manipulation GitKraken

Le logiciel GitKraken offre une interface de gestion git avec un dépôt distant. Il permet de contourner les lignes de commandes du terminal. 

## Télécharger GitKraken

La première étape est de télécharger le logiciel. Veuillez suivre les instructions proposées par https://www.gitkraken.com/ et télécharger la versions du logiciel qui correspond à votre ordinateur. 

## Connexion et clonage du dépôt 

Vous pouvez vous connecter à votre compte github depuis l'application. Celle ci vous redirigera vers le site internet Github pour valider la démarche. 

Une fois fait, vous devez cloner le dépôt centralisé pour pouvoir y accéder localement et travailler depuis votre ordinateur. 
Pour cela, il suffit de faire la suite d'opération suivante :  
  * Cliquer sur Clone un dépôt  
  * Aller dans l'onglet `Clone` puis `Github.com`.   
  * Si tout va bien, vous avez accès dans la case 'Repository to clone' à notre dépôt nommé NICOLAS-ENJALBERT/PIP2021_G2  
  * Choisir le dossier qui accueillera votre dépôt local  
  * Valider (Cloner)  

## Découverte de l'interface

Pour comprendre les possibilités de GitKraken et son interface vous pouvez vous référer au document _gitkraken-cheat-sheet-v1.6.pdf_. 

## Aller sur sa branche

Dans la partie Gauche de l'interface, vous trouverez l'onglet `Remote`, déroulez le et placez vous dans la branche qui vous est dédiée. Pour cela faire un clic droit et accéder à `Checkout yourBranch` avec yourBranch qui est le nom de votre branche. 

## Travail

Avant de travailler, et à chaque début de journée, voir de demi journée, veuillez faire un pull en cliquant sur le bouton dédié dans le bandeau supérieur de l'interface. 

Vous pouvez travailler et faire vos diverses modifications sur votre branche ouverte :  
  - créer de nouveaux fichiers  
  - créer de nouveaux dossiers et sous dossiers  
  - modifier des fichiers existants  
  - etc ...  

## Soumettre vos modifications sur le serveur central et les partager avec vos collaborateurs. 

Vos fichiers modifiés, vous aurez une notification dans la colonne droite de l'interface. La première étape est de faire un `pull` dans le bandeau supérieur de l'interface.

Veuillez sélectionner vos fichiers à ajouter en cliquant sur `Stage all changes` ou en sélectionnant manuellement les fichiers avec `Stage file`. 
Veuillez vérifier que les fichiers que vous voulez soumettre se trouve bien dans la case `Staged files` et ne sont plus dans `Unstaged files`. 

Veuillez Inscrire un message explicatif pour nous permettre de comprendre les modifications que vous avez apporté. 

Il suffit maintenant d'appuyer sur `Commit change to x files`. 
Maintenant vous pouvez appuyer dans le bandeau haut sur le bouton `Push`. 

Votre modification est bien déposé sur le dépôt distant.


# Manipulation Git dans le terminal 

Ce chapitre permet de comprendre l'utilisation Git quand on utilise son terminal. 

## Cloner un dépôt distant  
Dans le cas du projet inter-promo, un dépôt a été créé et initié. Celui ci se trouve au lien suivant https://github.com/nicolas-enjalbert/pip2020_G2  ou sur le lien que votre chef vous indiquera. En suivant ce lien, vous trouverez la version en ligne du dépôt sous l'interface de Github.  
Pour travailler depuis votre ordinateur, il faut commencer par créer une copie de ce dépôt sur votre ordinateur. 
Pour ce faire veuillez ouvrir votre terminal et se placer dans le dossier qui accueillera le dossier git. Pour cela deux possibilités :  
	- ouvrir le terminal et se déplacer vers le dossier correspondant avec la commande `cd`  
	- ouvrir le terminal directement à partir du gestionnaire de fichier en faisant un "clic+droit"

Une fois cela taper la ligne `git clone https://github.com/nicolas-enjalbert/pip2020_G2.git`

## Changer de branche

Pour ne pas se marcher dessus et faciliter le partage des fichiers entre les collaborateurs chacun travaillera dans la branche qui lui sera attribuée. 

L'instruction `git checkout yourBranch` permet d'aller sur la branche nommée yourBranch. 

Une façon de savoir si cela a marché :  
  * se placer dans le dossier local du git avant la manipulation  
  * faire la manipulation sur le terminal  
  * retourner dans le gestionnaire de fichier et constater que les fichiers et sous dossier ont changé  

Votre branche est ouverte et les fichiers distant de cette branche sont copié sur votre ordinateur. Vous n'aurez accès qu'à ces documents tant que vous ne changerez pas de branche.

## Travailler et modifier vos fichiers 

La première chose à faire est de mettre à jour votre dépot. On va faire un pull : `git pull`. Si vous avez le message 'Already up-to-date.' alors tout est bon et la votre dossier local est prêt au travail 

Vous pouvez travailler et faire vos diverses modifications sur votre branche ouverte :  
  - créer de nouveaux fichiers  
  - créer de nouveaux dossiers et sous dossiers  
  - modifier des fichiers existants 
  - etc ...

## Partager les fichiers sur le dépôt centralisé
 
Une fois votre travail effectué où à la fin de la journée, il est temps de partager le travail que vous avez fait ! :) 
Une série d'action est nécessaire pour faire cela. 

Dans un premier temps il peut être judicieux de faire un `git status` pour savoir où en est le dépôt. Si vous n'avez pas de message d'erreur ou rien ne contre indiquant que votre git n'est pas à jour nous pouvons continuer. 

Pour ne pas avoir de conflit, veuillez faire un pull. Pour rappel cela se faisait aisément avec la commande `git pull`. Avec le message 'Already up-to-date.' vous pouvez continuer vous n'avez pas de conflit.

Il est nécessaire dans un premier temps de faire un 'add'. Une commande simple le permet : `git add - A`. 
Il est temps d'encapsuler les modifications dans un commit. Ce commit doit nécessairement comporter un message ('yourMessage') qui permettra de comprendre les modifications et retrouver facilement les versions. 
Pour cela faire : `git commit -m "yourMessage"`


On est presque arrivé au bout : il ne faut plus qu'envoyer les modifications au dépôt central. 
`git push` permettra de le faire. 

Si vous n'avez pas de message d'erreur alors tout va bien ! Félicitations 



  
