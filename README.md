# 🛡️ SentinelAI

**SIEM intelligent avec analyse d'alertes par IA locale**

SentinelAI est un système de détection et d'analyse de menaces de sécurité qui combine Wazuh (SIEM open-source) avec l'intelligence artificielle locale (Ollama) pour automatiser l'analyse des incidents de sécurité.

---

## 🎯 Fonctionnalités

- ✅ **Architecture SIEM complète** basée sur Wazuh (Manager, Indexer, Dashboard)
- ✅ **Analyse automatique par IA** des alertes de sécurité avec recommandations contextualisées
- ✅ **Détection de vulnérabilités** (CVE) avec scoring CVSS
- ✅ **API REST Wazuh** intégrée avec authentification JWT
- ✅ **IA locale** (Ollama/llama3.2) - aucune dépendance cloud, 100% gratuit

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Agent     │─────▶│   Manager    │─────▶│  Indexer    │
│  (Windows)  │      │  (Analyse)   │      │(Elasticsearch)│
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            ▼                      ▼
                     ┌──────────────┐      ┌─────────────┐
                     │  SentinelAI  │◀─────│  Dashboard  │
                     │  (IA Locale) │      │   (Web UI)  │
                     └──────────────┘      └─────────────┘
```

**Flux de données :**
1. L'agent collecte les événements système (Event Viewer, logs, etc.)
2. Le manager analyse et corrèle les événements selon les règles de détection
3. Les alertes sont indexées dans Elasticsearch
4. SentinelAI récupère les alertes via l'API REST
5. L'IA locale (Ollama) analyse chaque alerte et génère des recommandations

---

## 🛠️ Technologies utilisées

| Composant | Technologie |
|-----------|-------------|
| **SIEM** | Wazuh 4.x |
| **Conteneurisation** | Docker, Docker Compose |
| **Backend** | Python 3.11+ |
| **IA locale** | Ollama (llama3.2) |
| **API** | REST, JWT |
| **Base de données** | Elasticsearch |
| **Agents** | Wazuh Agent (Windows) |

---

## 📦 Installation

### Prérequis

- Docker Desktop
- Python 3.11+
- Ollama ([ollama.com](https://ollama.com))
- 8 GB RAM minimum

### 1. Cloner le projet

```bash
git clone https://github.com/<ton-username>/SentinelAI.git
cd SentinelAI
```

### 2. Déployer Wazuh avec Docker

```bash
cd infra/single-node
docker-compose up -d
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 4. Installer Ollama et télécharger le modèle

```bash
# Installer Ollama depuis https://ollama.com/download
ollama pull llama3.2
```

### 5. Configurer les credentials

Créer un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
# Éditer .env avec vos credentials Wazuh
```

---

## 🚀 Utilisation

### Lancer l'analyse d'alertes

```bash
python sentinel_ai.py
```

**Résultat :**

```
============================================================
SENTINEL AI - Analyse d'alertes Wazuh avec IA
============================================================

[1/4] Connexion a Wazuh...
  [OK] Authentification reussie

[2/4] Recuperation des alertes...
  [OK] 5 alertes recuperees

[3/4] Initialisation de l'IA...
  [OK] Modele llama3.2 pret

[4/4] Analyse des alertes avec l'IA...
------------------------------------------------------------

[ALERTE 1/5]
  Description: Windows Logon Failure
  Niveau: 5/15
  Agent: Windows-PC

  [ANALYSE IA]
    Gravite: MEDIUM
    Explication: Tentative de brute force détectée
    Recommandations:
      - Bloquer l'IP source après 5 tentatives
      - Activer l'authentification à deux facteurs
```

---

## 📁 Structure du projet

```
SentinelAI/
├── src/
│   ├── wazuh_client.py       # Client API Wazuh
│   ├── alert_analyzer.py     # Analyseur IA
│   └── test_alerts.py        # Alertes de test
├── infra/
│   └── single-node/          # Configuration Docker Wazuh
├── data/                     # Données et logs
├── sentinel_ai.py            # Script principal
├── requirements.txt          # Dépendances Python
├── .env.example              # Template de configuration
└── README.md                 # Documentation
```

---

## 📊 Exemple d'analyse IA

**Alerte détectée :**
```json
{
  "rule": {
    "description": "CVE-2019-15315 affects setuptools",
    "level": 10
  },
  "agent": {
    "name": "Windows-PC"
  }
}
```

**Analyse SentinelAI :**
```json
{
  "severity": "critical",
  "explanation": "Vulnérabilité critique affectant setuptools, exige une mise à jour immédiate",
  "recommendations": [
    "Mettre à jour setuptools vers la dernière version",
    "Exécuter une analyse de sécurité supplémentaire"
  ],
  "is_false_positive": false
}
```

---

## 🔮 Roadmap

### Phase 1 : Connexion aux données réelles (En cours)
- [ ] **Connexion à l'indexer Elasticsearch** (port 9200) pour récupérer les alertes en temps réel
- [ ] **Parser les alertes Wazuh** directement depuis l'indexer avec requêtes DSL
- [ ] **Support multi-agents** : analyser les alertes de plusieurs machines simultanément
- [ ] **Persistance des analyses** : stocker les résultats dans une base SQLite

### Phase 2 : Interface utilisateur et visualisation
- [ ] **Dashboard web interactif** (Flask + Chart.js)
  - Métriques en temps réel : nombre d'alertes par gravité
  - Graphiques de tendances (dernières 24h, 7 jours, 30 jours)
  - Top 10 des vulnérabilités détectées
  - Carte de chaleur des heures d'activité suspecte
- [ ] **Interface de gestion des alertes** : marquer comme traitée, faux positif, etc.
- [ ] **Historique des analyses IA** : consulter les anciennes recommandations

### Phase 3 : Automatisation et notifications
- [ ] **Système de notifications automatiques**
  - Email pour alertes critiques (niveau ≥ 10)
  - Intégration Slack/Discord pour alertes en temps réel
  - SMS via Twilio pour incidents majeurs
- [ ] **Rapports automatisés**
  - Rapport de sécurité hebdomadaire en PDF
  - Statistiques mensuelles avec graphiques
  - Export CSV pour analyse externe
- [ ] **Actions automatiques** : bloquer une IP suspecte, isoler un agent compromis

### Phase 4 : Intelligence avancée
- [ ] **Corrélation multi-sources** : détecter les attaques coordonnées
  - Exemple : Failed login (PC A) + Port scan (PC B) = Attaque distribuée
- [ ] **Intégration framework MITRE ATT&CK**
  - Mapper chaque alerte aux tactiques/techniques MITRE
  - Générer des kill chains d'attaques
- [ ] **Machine Learning** : détection d'anomalies comportementales
  - Baseline du comportement normal de chaque agent
  - Alertes sur écarts significatifs (nouveau processus, trafic inhabituel)
- [ ] **Threat Intelligence** : enrichir avec des flux externes
  - Vérifier les IP suspectes contre des bases de réputation (AbuseIPDB, VirusTotal)
  - Ajouter le contexte géographique (pays d'origine de l'attaque)

### Phase 5 : Scalabilité et production
- [ ] **Support de multiples modèles IA** : comparer llama3.2, mistral, deepseek
- [ ] **Mode API** : exposer SentinelAI comme service REST
- [ ] **Conteneurisation** : Docker pour SentinelAI lui-même
- [ ] **CI/CD** : tests automatisés, déploiement continu
- [ ] **Documentation technique** : API reference, guide d'architecture
- [ ] **Mode distribué** : analyser 100+ agents avec load balancing

---

## 📚 Documentation complémentaire

- [OUTILS_ET_COMMANDES.md](OUTILS_ET_COMMANDES.md) - Guide complet des outils et commandes utilisés
- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Ollama Documentation](https://ollama.com/)

---

## 🤝 Contribution

Projet personnel d'apprentissage en cybersécurité. Les suggestions et retours sont les bienvenus !

---

## 📝 Licence

MIT License - Projet éducatif

---

## 👨‍💻 Auteur

Développé dans le cadre d'un apprentissage approfondi des systèmes SIEM et de l'intégration de l'IA dans la cybersécurité.
