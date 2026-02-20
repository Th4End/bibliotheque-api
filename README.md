# 📚 Bibliotheque API

Une API RESTful moderne pour la gestion d'une bibliothèque, construite avec **FastAPI** et **PostgreSQL**.

## Aperçu

Bibliotheque API est une application backend robuste permettant de gérer les livres, les utilisateurs et les tags associés. Elle fournit une interface API complète pour les opérations CRUD (Create, Read, Update, Delete) sur les ressources principales d'une bibliothèque.

### Caractéristiques principales

- ✅ Gestion des livres
- ✅ Gestion des utilisateurs  
- ✅ Système de tags/catégories
- ✅ Base de données PostgreSQL
- ✅ Validation des données avec Pydantic
- ✅ Documentation API automatique avec Swagger UI

---

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python** ≥ 3.11.9
- **PostgreSQL** ≥ 12
- **uv** pour la gestion des dépendances
- **Git** 

### Installation de uv

**Windows** (avec winget) :
```powershell
winget install astral-sh.uv
```
**macOS / Linux** :
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd bibliotheque-api
```
### 2. Installer les dépendances

```bash
uv sync
```

Cette commande créera automatiquement un environnement virtuel (`.venv`) et installera toutes les dépendances.

### 3. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql://user:password@localhost:5432/bibliotheque
```
### 4. Initialiser la base de données

```bash
python -m app.main
```
---
## Structure du projet
```
├── app
│   ├── core
│   │   ├── auth.py
│   │   └── security.py
│   ├── models
│   │   ├── Books.py
│   │   ├── tags.py
│   │   └── users.py
│   ├── routers
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── tags.py
│   │   └── users.py
│   ├── schemas
│   │   ├── Books.py
│   │   ├── tags.py
│   │   └── users.py
│   ├── database.py
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```
---

## API Endpoints

### Livres (`/books`)
- `GET /books/` - Récupérer tous les livres

### Utilisateurs (`/users`)
- `GET /users/` - Récupérer tous les utilisateurs

### Tags (`/tags`)
- `GET /tags/` - Récupérer tous les tags

### Root
- `GET /` - Message de bienvenue

---

## ▶️ Exécution de l'application

### Démarrer le serveur de développement

```bash
uvicorn app.main:app --reload
```

L'application sera disponible à : `http://localhost:8000`

### Accéder à la documentation API

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

## Dépendances

| Package | Version | Utilité |
|---------|---------|---------|
| FastAPI | ≥0.128.0 | Framework web asynchrone |
| SQLAlchemy | ≥2.0.46 | ORM pour interactions BD |
| Psycopg | ≥3.3.2 | Driver PostgreSQL |
| Pydantic | ≥2.12.5 | Validation de données |
| Uvicorn | ≥0.40.0 | Serveur ASGI |
| python-dotenv | ≥1.2.1 | Gestion variables d'environnement |
| python-jose | ≥3.5.0 | gestion du jwt |
---

## Architecture

L'application suit une architecture **modulaire en couches** :

1. **Routers** : Points d'entrée HTTP
2. **Models** : Schémas de base de données (SQLAlchemy)
3. **Database** : Configuration de la connexion et sessions
4. **Main** : Inicialisation FastAPI et configuration globale
---

## Support

Pour toute question ou problème, veuillez ouvrir une issue dans le repository.