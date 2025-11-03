# Conversation AI Application

Une application de conversation utilisant OpenAI et Streamlit.

## Configuration locale

1. Clonez le dépôt :
```bash
git clone https://github.com/niangmamath/conversation.git
cd conversation
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement :
   - Copiez le fichier `env-sample.txt` vers `.env`
   - Ajoutez votre clé API OpenAI dans le fichier `.env`

## Déploiement sur Streamlit Cloud

Pour déployer sur Streamlit Cloud :

1. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io/)
2. Déployez depuis votre dépôt GitHub
3. Dans les paramètres de l'application :
   - Allez dans "Settings" > "Secrets"
   - Ajoutez la variable d'environnement `OPENAI_API_KEY` avec votre clé API OpenAI

## Variables d'environnement requises

- `OPENAI_API_KEY` : Votre clé API OpenAI

## Exécution locale

```bash
streamlit run app.py
```
