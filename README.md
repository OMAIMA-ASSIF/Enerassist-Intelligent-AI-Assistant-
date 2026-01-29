# 🤖 AI Chatbot Fullstack (FastAPI + React + LangChain)

Ce projet est un chatbot IA complet spécialisé dans le dépannage technique des vannes, utilisant une architecture RAG (Retrieval-Augmented Generation) avec Mistral AI et Qdrant.

---

## 🚀 Installation Rapide

### 1. Cloner le projet
```powershell
git clone <url-du-repo>
cd CHATBOT_H15
```

---

## 🏗️ Configuration du Backend (FastAPI)

Le backend gère l'authentification, l'historique des conversations et l'intelligence artificielle.

### 1. Créer l'environnement virtuel
```powershell
python -m venv venv
# Activer sur Windows (PowerShell) :
.\venv\Scripts\Activate.ps1
```

### 2. Installer les dépendances
```powershell
pip install -r requirements.txt
```

### 3. Configuration des variables d'environnement
Vous devez créer **deux** fichiers `.env` :

*   **Fichier 1 : `./server/.env`**
    ```env
    MONGO_URI=votre_uri_mongodb_atlas
    SECRET_KEY=votre_clé_secrète_jwt
    ```
*   **Fichier 2 : `./ai/.env`**
    ```env
    MISTRAL_API_KEY=votre_clé_mistral
    QDRANT_URL=votre_url_qdrant
    QDRANT_API_KEY=votre_clé_qdrant
    ```

### 4. Lancer le Backend
Depuis la racine du projet (`CHATBOT_H15`), utilisez cette commande robuste :
```powershell
.\venv\Scripts\python -m uvicorn main:app --reload
```
L'API sera disponible sur : `http://localhost:8000`

---

## 💻 Configuration du Frontend (React + Vite)

Le frontend est une interface moderne et réactive.

### 1. Accéder au dossier client
```powershell
cd client
```

### 2. Installer les paquets
```powershell
npm install
```

### 3. Lancer le projet
```powershell
npm run dev
```
L'interface sera disponible sur : `http://localhost:5173` (ou 3000 selon votre config).

---

## 📂 Structure du Projet

*   `server/` : Logique FastAPI, Authentification (JWT), et modèles de données.
*   `ai/` : Moteur de l'IA, intégration LangChain et base de données vectorielle Qdrant.
*   `client/` : Application React avec TailwindCSS/CSS moderne.
*   `main.py` : Point d'entrée principal de l'API.

---

## 💡 Notes Importantes (Windows / PowerShell)

*   **Erreur de Scripts** : Si PowerShell bloque l'activation du `venv`, lancez une fois :
    `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
*   **MongoDB** : Assurez-vous d'avoir ajouté votre adresse IP dans la section **Network Access** de votre dashboard MongoDB Atlas.
