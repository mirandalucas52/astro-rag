# Astro Rag

Ce projet implémente un assistant de chat interactif qui utilise l'API Ollama pour générer des réponses contextuelles en se basant sur des embeddings de contenu. L'assistant peut réécrire les requêtes des utilisateurs et fournir des réponses en fonction du contexte extrait d'un fichier de contenu (le "vault").

## Fonctionnalités principales
- **Génération d'embeddings** : Crée et charge des embeddings pour le contenu du vault à l'aide de l'API Ollama.
- **Réécriture des requêtes** : Réécrit les requêtes de l'utilisateur pour améliorer la précision et la clarté des questions.
- **Récupération du contexte** : Extrait le contexte pertinent à partir des embeddings pour enrichir les réponses.
- **Chat interactif** : Permet à l'utilisateur de poser des questions et de recevoir des réponses contextuelles.

## Prérequis
Avant de commencer, vous devez avoir installé les dépendances suivantes :
- **Python 3.x**

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/mirandalucas52/astro-rag.git
   cd astro-rag

2. Installez les dépendances nécessaires :

   pip install -r requirements.txt

Assurez-vous que l'API Ollama et (optionnellement) OpenAI sont correctement configurées pour le projet.

## Utilisation

1. Vous devez tout d'abord mettre l'ID du fichier pdf se situant dans votre Google Drive à la ligne 6 du fichier upload.py.

Pour l'exemple, nous avons un fichier sur l'astrologie, vous pouvez run le projet en faisant la commande

    python astro.py

Vous pourrez poser une question à ollama, si vous faites la commande :

    python upload.py

Avant de lancer le script astro.py, vous allez charger des embeddings pour le contenu du vault, ce qui va permettre à votre chat interactif d'être plus précis sur sa réponse en allant chercher le contenu dans le fichier PDF envoyé.