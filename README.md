# 🤖 AI Technical Assistant & Incident Management (HI5)

Ce projet est un chatbot intelligent spécialisé dans le **dépannage technique industriel** (électrovannes et vannes de zone). Il utilise une architecture **RAG (Retrieval-Augmented Generation)** pour fournir des réponses précises basées sur une documentation technique, et intègre un système de **ticketing Jira automatique** en cas d'échec de résolution.

---

## ✨ Fonctionnalités Clés

*   **🔍 Recherche Intelligente (RAG)** : Utilise Qdrant et LangChain pour extraire des informations pertinentes de la documentation technique.
*   **🛠️ Diagnostic Expert** : Assistance spécialisée dans l'installation, la maintenance et le dépannage de composants pneumatiques.
*   **🎟️ Intégration Jira Automatique** : Si l'IA ne peut pas résoudre le problème, elle propose et crée automatiquement un ticket Jira avec la priorité appropriée par le serveur MCP .
*   **💬 Gestion des Conversations** : Historique complet, gestion des favoris et thèmes personnalisables.
*   **🔐 Authentification Sécurisée** : Système robuste basé sur JWT et FastAPI.

---
## 📺 Démonstration du projet HI5
<video src="https://github.com/OMAIMA-ASSIF/Enerassist-Intelligent-AI-Assistant-/blob/main/demo-%20Enerassist.mp4" controls width="100%">
  Votre navigateur ne supporte pas la lecture de vidéos.
</video>


## 🏗️ Stack Technique

### Backend (Python)
*   **FastAPI** : Framework principal pour l'API.
*   **MongoDB (Motor)** : Stockage des utilisateurs, conversations et historiques.
*   **LangChain** : Orchestration de la logique IA et des outils.
*   **Mistral AI** : Modèle de langage (LLM) performant utilisé pour le raisonnement.
*   **Qdrant** : Base de données vectorielle pour la recherche sémantique.

### Frontend (React)
*   **Vite** : Outil de build ultra-rapide.
*   **Tailwind CSS & Framer Motion** : Pour une interface moderne, fluide et responsive.
*   **Axios** : Communication avec l'API backend.

### Intégration (MCP)
*   **Model Context Protocol (MCP)** : Utilisé pour connecter l'IA aux outils Atlassian (Jira) de manière modulaire.

---

## 📂 Structure du Projet

```text
├── server/             # Backend FastAPI (Auth, Routes, Services)
├── ai/                 # Logique IA (LangChain, RAG, MCP Bridge)
│   └── mcp-nodejs-atlassian/  # Serveur MCP pour Jira/Atlassian
├── client/             # Frontend React (Pages, Components, Context)
├── main.py             # Point d'entrée principal du backend
├── requirements.txt    # Dépendances Python
└── README.md           # Ce guide !
```

---

## 🛠️ Installation & Configuration

### 1. Prérequis
*   Python 3.10+
*   Node.js 18+
*   MongoDB Atlas (ou instance locale)
*   Compte Cloud Qdrant
*   Clé API Mistral AI
*   Compte Atlassian (pour Jira)

### 2. Configuration du Backend
1.  **Environnement Virtuel** :
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```
2.  **Variables d'environnement** :
    Créez un fichier `.env` dans le dossier `server/` :
    ```env
    MONGO_URI=votre_uri_mongodb
    SECRET_KEY=votre_cle_secrete_jwt
    ```
    Créez un fichier `.env` dans le dossier `ai/` :
    ```env
    QDRANT_URL=votre_url_qdrant
    QDRANT_API_KEY=votre_cle_qdrant
    MISTRAL_API_KEY=votre_cle_mistral
    ```

### 3. Ingestion des Données (RAG)
Avant la première utilisation du chatbot, vous devez transformer les documents techniques en vecteurs dans Qdrant. 
> [!IMPORTANT]
> Cette étape ne doit être exécutée **qu'une seule fois** (ou lors d'une mise à jour de la documentation).

1.  **Exécuter l'ingestion** :
    ```powershell
    cd ai
    python ingest_data.py
    ```

### 4. Configuration du Serveur MCP (Jira)
Allez dans `ai/mcp-nodejs-atlassian/` et installez les dépendances :
```bash
npm install
```
Créez un fichier `.env` dans ce dossier avec vos identifiants Atlassian :
```env
JIRA_URL=https://votre-site.atlassian.net
JIRA_USERNAME=votre-email@exemple.com
JIRA_API_TOKEN=votre_token_api_atlassian
ATLASSIAN_EMAIL=ton-email-atlassian
ATLASSIAN_API_TOKEN=


```

### 5. Configuration du Frontend
Allez dans le dossier `client/` :
```bash
npm install
npm run dev
```

---

## 🚀 Lancement du Projet

1.  **Démarrer le Backend** :
    ```powershell
    python -m uvicorn main:app --reload
    ```
2.  **Démarrer le Frontend** :
    ```bash
    cd client
    npm run dev
    ```

L'application sera disponible sur `http://localhost:5173`.

---

## 📖 Utilisation

1.  **Connexion** : Créez un compte ou connectez-vous.
2.  **Chat** : Posez vos questions techniques sur les vannes (ex: "Ma vanne V-12 fuit, que faire ?").
3.  **Dépannage** : Suivez les instructions de l'IA.
4.  **Ticketing** : Si le problème n'est pas résolu, dites "Rien ne marche" ou demandez un ticket. L'IA créera alors une demande dans votre Jira avec les détails techniques.

