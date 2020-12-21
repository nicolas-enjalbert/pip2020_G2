---
title: Manipulation technique pour Github
author: Nicolas Enjalbert Courrech 
Date:     November 8, 2020 
---

Ce fichier est une aide mémoire, tutoriel pour l'utilisation de Github et ses interfaces possibles : GitKraken et le terminal de votre ordinateur.


# Manipulation Git dans le terminal 

Ce chapitre permet de comprendre l'utilisation Git quand on utilise son terminal. 

## Cloner un dépôt distant  
Dans le cas du projet interpromo, un dépôt a été créé et initié. Celui ci se trouve au lien suivant https://github.com/nicolas-enjalbert/pip2020_G2 . En suivant ce lien, vous trouverez la version en ligne du dépôt sous l'interface de github.  
Pour travailler depuis votre ordinateur, il faut commencer par créer une copie de ce dépôt sur votre ordinateur. 
Pour ce faire veuillez ouvrir votre terminal et se placer dans le dossier qui accueillera le dossier git. Pour cela deux possibilités :  
	- ouvrir le terminal et se déplacer vers le dossier correspondant avec la commande `cd`  
	- ouvrir le terminal directement à partir du gestionnaire de fichier en faisant un "clic+droit"

Une fois cela taper la ligne `git clone https://github.com/nicolas-enjalbert/pip2020_G2.git`

## Changer de branche

Pour ne pas se marcher dessus et faciliter le partage des fichiers entre les collaborateurs chacun travaillera dans la branche qui lui sera attribuée. 

L'instruction `git checkout yourBranch` permet d'aller sur la branche nommée yourBranch. 

Une façon de savoir si cela a marché :  
  * se placer dans le dossier local du git avant la maniuplation  
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

Dans un premier temps il peut etre judicieux de faire un `git status` pour savoir où en est le dépot. Si vous n'avez pas de message d'erreur ou rien ne contre indiquant que votre git n'est pas à jour nous pouvons continuer. 

Pour ne pas avoir de conflit, veuillez faire un pull. Pour rappel cela se faisait aisément avec la commande `git pull`. Avec le message 'Already up-to-date.' vous pouvez continuer vous n'avez pas de conflit.

Il est nécessaire dans un premier temps de faire un 'add'. Une commande simple le permet : `git add - A`. 
Il est temps d'encapsuler les modifications dans un commit. Ce commit doit nécessairement comporter un message ('yourMessage') qui permettra de comprendre les modifications et retrouver facilement les versions. 
Pour cela faire : `git commit -m "yourMessage"`


On est presque arrivé au bout : il ne faut plus qu'envoyer les modifications au dépôt central. 
`git push` permettra de le faire. 

Si vous n'avez pas de message d'erreur alors tout va bien ! Félicitations 



  

