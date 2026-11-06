# 🛠️ Outils et Commandes — SentinelAI

Documentation complète des outils, bibliothèques et commandes utilisés dans le projet.

---

## 📚 Table des matières

1. [Outils Système](#outils-système)
2. [Bibliothèques Python](#bibliothèques-python)
3. [API et Services](#api-et-services)
4. [Commandes Docker](#commandes-docker)
5. [Commandes Git](#commandes-git)
6. [IA et Machine Learning](#ia-et-machine-learning)

---

## 🖥️ Outils Système

### Docker Desktop

**Qu'est-ce que c'est ?**
- Plateforme pour exécuter des conteneurs (applications isolées)
- Permet de déployer Wazuh sans installer manuellement tous les composants

**Pourquoi on l'utilise ?**
- Wazuh a 3 composants (Manager, Indexer, Dashboard) → Docker les gère tous
- Isolation : Les conteneurs ne polluent pas ton système Windows
- Reproductibilité : Même environnement sur n'importe quelle machine

**Commandes principales :**
```bash
# Voir les conteneurs en cours d'exécution
docker ps

# Voir tous les conteneurs (actifs + arrêtés)
docker ps -a

# Voir les logs d'un conteneur
docker logs <nom_conteneur>

# Arrêter un conteneur
docker stop <nom_conteneur>

# Démarrer un conteneur arrêté
docker start <nom_conteneur>

# Redémarrer un conteneur
docker restart <nom_conteneur>
```

**Exemple concret :**
```bash
docker logs single-node-wazuh.manager-1 --tail 50
# Affiche les 50 dernières lignes de logs du manager Wazuh
```

---

### Docker Compose

**Qu'est-ce que c'est ?**
- Outil pour gérer plusieurs conteneurs Docker en même temps
- Utilise un fichier `docker-compose.yml` pour la configuration

**Pourquoi on l'utilise ?**
- Wazuh a 3 conteneurs qui doivent communiquer entre eux
- Docker Compose les démarre tous ensemble avec les bonnes configurations

**Commandes principales :**
```bash
# Démarrer tous les services (depuis le dossier avec docker-compose.yml)
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Voir les logs de tous les services
docker-compose logs

# Redémarrer tous les services
docker-compose restart
```

**Structure du projet Wazuh :**
```
infra/
└── single-node/
    └── docker-compose.yml  ← Fichier de configuration
```

---

### WSL (Windows Subsystem for Linux)

**Qu'est-ce que c'est ?**
- Linux intégré dans Windows
- Permet d'utiliser des commandes Linux sans dual-boot

**Pourquoi on l'utilise ?**
- Beaucoup d'outils de cybersécurité sont conçus pour Linux
- Python fonctionne mieux sur Linux pour certaines bibliothèques

**Commandes de base :**
```bash
# Ouvrir WSL
wsl

# Voir la version Linux
cat /etc/os-release

# Naviguer vers un dossier Windows
cd /mnt/c/Users/<username>/Projets/SentinelAI
```

---

## 🐍 Bibliothèques Python

### requests

**Qu'est-ce que c'est ?**
- Bibliothèque pour faire des requêtes HTTP/HTTPS en Python
- Alternative simple à `urllib` (bibliothèque standard, plus complexe)

**Pourquoi on l'utilise ?**
- Communication avec l'API Wazuh (récupérer alertes, agents, vulnérabilités)
- Syntaxe simple et intuitive

**Installation :**
```bash
pip install requests
```

**Exemple d'utilisation :**
```python
import requests

# Requête GET (récupérer des données)
response = requests.get("https://api.exemple.com/data")
data = response.json()  # Parse le JSON en dictionnaire Python

# Requête POST (envoyer des données)
response = requests.post(
    "https://api.exemple.com/login",
    json={"username": "user", "password": "pass"}
)
```

**Méthodes HTTP principales :**

| Méthode | Usage | Exemple SentinelAI |
|---------|-------|---------------------|
| `GET` | Récupérer des données | `get_alerts()`, `get_agents()` |
| `POST` | Créer/envoyer des données | `authenticate()` (envoyer credentials) |
| `PUT` | Mettre à jour une ressource | Modifier une config Wazuh |
| `DELETE` | Supprimer une ressource | Supprimer un agent |

**Paramètres importants :**

```python
requests.get(
    url="https://...",           # URL de l'API
    headers={"Authorization": "..."},  # Headers HTTP (authentification, etc.)
    params={"limit": 100},       # Query parameters (?limit=100)
    json={"key": "value"},       # Body JSON (pour POST/PUT)
    verify=False,                # Ignorer vérification SSL (certificats auto-signés)
    timeout=10                   # Timeout en secondes
)
```

**Gestion d'erreurs :**

```python
try:
    response = requests.get("https://...")
    response.raise_for_status()  # Lance une exception si erreur HTTP (400, 500, etc.)
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"Erreur HTTP: {e}")
except requests.exceptions.Timeout:
    print("Timeout: Le serveur met trop de temps à répondre")
except requests.exceptions.ConnectionError:
    print("Erreur de connexion: Impossible de joindre le serveur")
```

---

### urllib3

**Qu'est-ce que c'est ?**
- Bibliothèque sous-jacente de `requests`
- Gère les connexions HTTP de bas niveau

**Pourquoi on l'utilise ?**
- Désactiver les warnings SSL pour les certificats auto-signés de Wazuh

**Exemple :**
```python
import urllib3

# Désactive les warnings SSL (sinon, ton terminal est pollué de messages)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

**⚠️ Attention :**
- Ne jamais faire ça en production sur Internet (risque de sécurité)
- OK pour Wazuh local avec certificat auto-signé

---

### python-dotenv

**Qu'est-ce que c'est ?**
- Charge les variables d'environnement depuis un fichier `.env`

**Pourquoi on en aura besoin ?**
- Stocker les secrets (mots de passe, clés API) hors du code
- Éviter de commit les credentials sur Git

**Installation :**
```bash
pip install python-dotenv
```

**Exemple d'utilisation :**

**Fichier `.env` :**
```env
WAZUH_API_URL=https://localhost:55000
WAZUH_API_USER=wazuh-wui
WAZUH_API_PASSWORD=your_password_here
```

**Code Python :**
```python
from dotenv import load_dotenv
import os

# Charge les variables du fichier .env
load_dotenv()

# Récupère les valeurs
api_url = os.getenv("WAZUH_API_URL")
username = os.getenv("WAZUH_API_USER")
password = os.getenv("WAZUH_API_PASSWORD")
```

---

## 🤖 IA et Machine Learning

### Ollama

**Qu'est-ce que c'est ?**
- Logiciel pour exécuter des modèles d'IA **localement** (sur ton PC)
- Gratuit et open-source
- Alternative locale à ChatGPT, Claude, etc.

**Pourquoi on va l'utiliser ?**
- Analyser les alertes Wazuh avec l'IA
- Détecter des patterns suspects
- Générer des recommandations de sécurité
- **100% gratuit, pas besoin de clé API**

**Installation (Windows) :**
1. Télécharger : [https://ollama.com/download](https://ollama.com/download)
2. Installer l'exécutable
3. Vérifier l'installation :
```bash
ollama --version
```

**Modèles recommandés pour SentinelAI :**

| Modèle | Taille | RAM nécessaire | Usage |
|--------|--------|----------------|-------|
| `llama3.2` | 2 GB | 8 GB | Analyse rapide d'alertes |
| `mistral` | 4 GB | 8 GB | Analyse approfondie |
| `deepseek-r1:1.5b` | 1 GB | 4 GB | Ultra léger (si PC limité) |

**Télécharger un modèle :**
```bash
ollama pull llama3.2
```

**Tester Ollama :**
```bash
ollama run llama3.2
>>> Analyse cette alerte: Failed login attempt from IP 192.168.1.50
```

**Utiliser Ollama en Python :**

**Installation de la bibliothèque :**
```bash
pip install ollama
```

**Code Python :**
```python
import ollama

# Analyser une alerte
response = ollama.chat(
    model="llama3.2",
    messages=[{
        "role": "user",
        "content": "Analyse cette alerte Wazuh: Multiple failed login attempts from IP 192.168.1.50"
    }]
)

print(response['message']['content'])
```

**Exemple de réponse IA :**
```
Cette alerte indique une tentative de brute force sur un compte utilisateur.
Recommandations:
1. Bloquer l'IP 192.168.1.50 temporairement
2. Vérifier si le compte ciblé existe
3. Activer l'authentification à deux facteurs
4. Surveiller cette IP pour d'autres tentatives
```

---

### Alternatives à Ollama (si PC trop lent)

#### LM Studio
- Interface graphique pour exécuter des modèles IA
- Plus simple qu'Ollama pour débuter
- Téléchargement : [https://lmstudio.ai/](https://lmstudio.ai/)

#### API externes (payantes)
- **OpenAI GPT-4** : Le plus puissant, mais payant (~$0.03 par requête)
- **Anthropic Claude** : Très bon en analyse, payant
- **Google Gemini** : Version gratuite disponible

---

## 🔐 API et Services

### API Wazuh

**Qu'est-ce que c'est ?**
- Interface de programmation pour interagir avec Wazuh
- Permet de récupérer alertes, agents, vulnérabilités sans l'interface web

**Endpoints principaux :**

| Endpoint | Méthode | Description | Notre méthode |
|----------|---------|-------------|---------------|
| `/security/user/authenticate` | POST | S'authentifier et obtenir un token JWT | `authenticate()` |
| `/agents` | GET | Liste des agents connectés | `get_agents()` |
| `/alerts` | GET | Alertes de sécurité récentes | `get_alerts()` |
| `/vulnerability/{agent_id}` | GET | Vulnérabilités d'un agent | `get_vulnerabilities()` |
| `/sca/{agent_id}` | GET | Résultats de Security Configuration Assessment | (à implémenter) |

**Authentification JWT :**

1. **Étape 1** : Envoyer `username` + `password` → Recevoir un `token`
2. **Étape 2** : Pour chaque requête suivante, envoyer `Authorization: Bearer <token>`

**Format du token JWT :**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Indhemgtd3VpIiwiaWF0IjoxNjk4NzY1NDMyLCJleHAiOjE2OTg3NjkwMzJ9.xyz123
```

**Structure :**
- `eyJ...` : Header (algorithme de signature)
- `.eyJ...` : Payload (données utilisateur)
- `.xyz123` : Signature (vérification d'intégrité)

**Durée de vie :** ~15 minutes (après, il faut se ré-authentifier)

---

### Paramètres de requête courants

**Pagination :**
```python
params = {
    "limit": 100,    # Nombre max de résultats
    "offset": 0      # Skip les N premiers résultats
}
```

**Tri :**
```python
params = {
    "sort": "-timestamp"  # Tri décroissant par timestamp
    # Autres exemples:
    # "sort": "name"       # Tri croissant par nom
    # "sort": "-cvss.score" # Tri décroissant par score CVSS
}
```

**Filtres :**
```python
params = {
    "rule.level": ">5",        # Niveau > 5
    "agent.name": "Windows-PC", # Agent spécifique
    "status": "active"          # Statut actif
}
```

---

## 🐳 Commandes Docker (résumé complet)

### Gestion des conteneurs

```bash
# Lister les conteneurs actifs
docker ps

# Lister tous les conteneurs
docker ps -a

# Démarrer un conteneur
docker start <nom_ou_id>

# Arrêter un conteneur
docker stop <nom_ou_id>

# Redémarrer un conteneur
docker restart <nom_ou_id>

# Supprimer un conteneur (il doit être arrêté)
docker rm <nom_ou_id>
```

### Logs et inspection

```bash
# Voir les logs
docker logs <nom_ou_id>

# Suivre les logs en temps réel
docker logs -f <nom_ou_id>

# Afficher les 50 dernières lignes
docker logs --tail 50 <nom_ou_id>

# Inspecter la configuration
docker inspect <nom_ou_id>

# Voir les stats (CPU, RAM)
docker stats
```

### Réseau

```bash
# Lister les réseaux Docker
docker network ls

# Inspecter un réseau
docker network inspect <nom_réseau>
```

### Nettoyage

```bash
# Supprimer les conteneurs arrêtés
docker container prune

# Supprimer les images inutilisées
docker image prune

# Nettoyage complet (conteneurs, réseaux, images, volumes)
docker system prune -a
```

---

## 📝 Commandes Git (pour versioning)

### Initialisation

```bash
# Initialiser un dépôt Git
git init

# Voir l'état des fichiers
git status

# Voir l'historique des commits
git log --oneline
```

### Commits

```bash
# Ajouter des fichiers au staging
git add src/wazuh_client.py

# Ajouter tous les fichiers modifiés
git add .

# Créer un commit
git commit -m "Ajout de la méthode get_vulnerabilities"

# Voir les différences non commitées
git diff
```

### Branches

```bash
# Lister les branches
git branch

# Créer une nouvelle branche
git branch feature/ia-analysis

# Changer de branche
git checkout feature/ia-analysis

# Créer et changer de branche en une commande
git checkout -b feature/ia-analysis
```

---

## 🧪 Environnement Python

### Création d'un environnement virtuel

**Pourquoi ?**
- Isoler les dépendances du projet
- Éviter les conflits entre projets

**Commandes :**

```bash
# Créer un environnement virtuel (venv)
python -m venv venv

# Activer l'environnement (Windows Git Bash)
source venv/Scripts/activate

# Activer l'environnement (PowerShell)
.\venv\Scripts\Activate.ps1

# Désactiver l'environnement
deactivate
```

### Gestion des dépendances

```bash
# Installer une bibliothèque
pip install requests

# Installer toutes les dépendances du projet
pip install -r requirements.txt

# Voir les bibliothèques installées
pip list

# Générer le fichier requirements.txt
pip freeze > requirements.txt
```

---

## 📊 PowerShell (Windows)

### Gestion des services

```bash
# Voir l'état du service Wazuh
Get-Service -Name "Wazuh"

# Démarrer le service
Start-Service -Name "Wazuh"

# Arrêter le service
Stop-Service -Name "Wazuh"

# Redémarrer le service
Restart-Service -Name "Wazuh"
```

### Navigation

```bash
# Lister les fichiers
ls

# Changer de dossier
cd C:\Users\<username>\Projets\SentinelAI

# Voir le dossier actuel
pwd

# Créer un dossier
mkdir nouveau_dossier
```

---

## 🔍 Concepts Importants

### f-strings (Python 3.6+)

**Qu'est-ce que c'est ?**
- Syntaxe pour insérer des variables dans des chaînes de caractères

**Exemples :**
```python
name = "User"
age = 25

# Sans f-string (ancien)
message = "Je m'appelle " + name + " et j'ai " + str(age) + " ans"

# Avec f-string (moderne)
message = f"Je m'appelle {name} et j'ai {age} ans"

# Expressions dans les f-strings
message = f"Dans 5 ans, j'aurai {age + 5} ans"
```

---

### JSON (JavaScript Object Notation)

**Qu'est-ce que c'est ?**
- Format de données textuelles pour échanger des informations
- Structure clé-valeur

**Exemple JSON :**
```json
{
  "agent": {
    "name": "Windows-PC",
    "id": "001",
    "status": "active"
  },
  "vulnerabilities": [
    {"cve": "CVE-2019-15315", "score": 8.8},
    {"cve": "CVE-2021-1234", "score": 7.5}
  ]
}
```

**Conversion JSON ↔ Python :**
```python
import json

# JSON string → Dictionnaire Python
json_string = '{"name": "User", "age": 25}'
data = json.loads(json_string)
print(data["name"])  # User

# Dictionnaire Python → JSON string
data = {"name": "User", "age": 25}
json_string = json.dumps(data)
print(json_string)  # {"name": "User", "age": 25}
```

---

### REST API

**Qu'est-ce que c'est ?**
- Architecture pour les API web
- Utilise les méthodes HTTP (GET, POST, PUT, DELETE)

**Principes :**
1. **Stateless** : Chaque requête est indépendante
2. **Ressources** : Tout est une ressource (agents, alertes, vulnérabilités)
3. **URIs** : Chaque ressource a une adresse unique

**Exemple :**
```
GET    /agents           → Liste tous les agents
GET    /agents/001       → Détails de l'agent 001
POST   /agents           → Créer un nouvel agent
PUT    /agents/001       → Modifier l'agent 001
DELETE /agents/001       → Supprimer l'agent 001
```

---

## 🎓 Ressources d'apprentissage

### Documentation officielle
- **Wazuh** : [https://documentation.wazuh.com/](https://documentation.wazuh.com/)
- **Docker** : [https://docs.docker.com/](https://docs.docker.com/)
- **Python requests** : [https://requests.readthedocs.io/](https://requests.readthedocs.io/)
- **Ollama** : [https://ollama.com/](https://ollama.com/)

### Tutoriels
- **REST API** : [https://restfulapi.net/](https://restfulapi.net/)
- **JSON** : [https://www.json.org/](https://www.json.org/)
- **Git** : [https://learngitbranching.js.org/](https://learngitbranching.js.org/)

---

## 📝 Checklist pour débuter

- [ ] Docker Desktop installé et fonctionnel
- [ ] Wazuh déployé (3 conteneurs actifs)
- [ ] Python 3.9+ installé
- [ ] Git installé
- [ ] Environnement virtuel Python créé
- [ ] Bibliothèque `requests` installée
- [ ] Ollama installé (pour l'IA)
- [ ] Modèle IA téléchargé (`ollama pull llama3.2`)

---

*Dernière mise à jour : 6 novembre 2026*
