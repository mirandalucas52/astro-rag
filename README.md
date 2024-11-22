# Astro Rag

Ce projet implémente un assistant de chat interactif qui utilise l'API Ollama pour générer des réponses contextuelles en se basant sur des embeddings de contenu. L'assistant peut réécrire les requêtes des utilisateurs et fournir des réponses en fonction du contexte extrait d'un fichier de contenu (le "vault").

## Fonctionnalités principales

-   **Génération d'embeddings** : Crée et charge des embeddings pour le contenu du vault à l'aide de l'API Ollama.
-   **Réécriture des requêtes** : Réécrit les requêtes de l'utilisateur pour améliorer la précision et la clarté des questions.
-   **Récupération du contexte** : Extrait le contexte pertinent à partir des embeddings pour enrichir les réponses.
-   **Chat interactif** : Permet à l'utilisateur de poser des questions et de recevoir des réponses contextuelles.

## Prérequis

Avant de commencer, vous devez avoir installé les dépendances suivantes :

-   **Python 3.x**
-   **Ollama**

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/mirandalucas52/astro-rag.git
    cd astro-rag

    ```

2. Installez les dépendances nécessaires :

    pip install -r requirements.txt

Assurez-vous que l'API Ollama et (optionnellement) OpenAI sont correctement configurées pour le projet.

## Utilisation

1. Vous devez tout d'abord mettre l'ID du fichier pdf se situant dans votre Google Drive à la ligne 6 du fichier upload.py.

Attention à bien mettre l'accès général de l'image à toutes les personnes possédant le lien et non uniquement en limité comme ci dessous :



<img width="505" alt="image" src="https://github.com/user-attachments/assets/f653091d-63da-450a-acd0-c6708a9c630c">



Pour l'exemple, nous avons un fichier sur l'astrologie, vous pouvez run le projet en faisant la commande suivante qui vous permettra d'avoir accès au chat interactif sans RAG.

    python astro.py

Si vous faites la commande avant de lancer le script astro.py :

    python upload.py

Vous allez charger des embeddings pour le contenu du vault, ce qui va permettre à votre chat interactif d'être plus précis sur sa réponse en allant chercher le contenu dans le fichier PDF envoyé.

Pour changer la temperature, vous pouvez aller ligne 62 du fichier astro.py et changer la valeur initiale de 0.1. Plus cette valeur est élevée, plus la réponse sera imprévisible et créative, plus elle est basse et plus la réponse sera précise et conservatrice.
