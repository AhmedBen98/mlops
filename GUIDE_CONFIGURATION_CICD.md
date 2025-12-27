# TP 4 MLOps - Configuration CI/CD avec GitHub Actions

**Date**: 27 décembre 2025  
**Auteur**: Ahmed Ben Abderrazak  
**Projet**: MLOps - Pipeline CI/CD avec MLflow et DVC

---

## Table des matières

1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Partie 1: Préparation du dépôt GitHub](#partie-1-préparation-du-dépôt-github)
4. [Partie 2: Configuration GitHub Actions](#partie-2-configuration-github-actions)
5. [Partie 3: Test et validation du pipeline](#partie-3-test-et-validation-du-pipeline)
6. [Partie 4: Traçabilité avec MLflow](#partie-4-traçabilité-avec-mlflow)
7. [Résolution des problèmes courants](#résolution-des-problèmes-courants)
8. [Conclusion](#conclusion)

---

## Introduction

Ce document décrit les étapes complètes pour mettre en place un pipeline CI/CD pour un projet MLOps utilisant:
- **GitHub Actions** pour l'automatisation
- **DVC** pour la gestion des données et pipelines
- **MLflow** pour le tracking des expérimentations
- **Scikit-learn** pour le machine learning

---

## Prérequis

### Logiciels requis
- Git installé sur votre machine
- Python 3.8+ installé
- Compte GitHub actif
- Un projet MLOps fonctionnel (avec DVC et MLflow)

### Connaissances requises
- Bases de Git et GitHub
- Notions de CI/CD
- Python et Machine Learning (scikit-learn)

---

## Partie 1: Préparation du dépôt GitHub

### Étape 1.1: Créer ou utiliser un dépôt GitHub existant

**Option A: Créer un nouveau dépôt**

1. Connectez-vous sur [GitHub](https://github.com)
2. Cliquez sur le bouton **"New"** ou **"+"** > **"New repository"**
3. Remplissez les informations:
   - **Repository name**: `mlops` (ou un nom de votre choix)
   - **Description**: "MLOps project with DVC, MLflow and CI/CD"
   - **Visibility**: Public ou Private
   - **Ne cochez PAS** "Add a README file" (vous avez déjà un README)
4. Cliquez sur **"Create repository"**

**Option B: Utiliser un dépôt existant**

Si vous avez déjà créé le dépôt: https://github.com/AhmedBen98/mlops.git

### Étape 1.2: Initialiser Git localement (si ce n'est pas déjà fait)

```bash
cd /home/abenabderrazak/Documents/mlops-mlflow-tp
git init
```

### Étape 1.3: Configurer le fichier .gitignore

Créez ou modifiez le fichier `.gitignore` pour exclure les fichiers sensibles:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
.venv/
venv/
ENV/

# MLflow
mlruns/

# DVC
/data/iris.csv
/data/processed/

# Models
*.pkl
model.pkl

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Logs
*.log
```

### Étape 1.4: Ajouter les fichiers au dépôt Git

**Important**: DVC utilise des fichiers `.dvc` pour tracker les données. N'ajoutez PAS les données réelles, seulement les fichiers `.dvc`.

```bash
# Ajouter tous les fichiers (en respectant .gitignore)
git add .

# Vérifier les fichiers qui seront ajoutés
git status
```

Fichiers qui **DOIVENT être** ajoutés:
- - `train.py`, `generate_iris.py`
- - `requirements.txt`
- - `dvc.yaml` (pipeline DVC)
- - `data/iris.csv.dvc` (metadata DVC)
- - `.dvc/` (configuration DVC)
- - `.github/workflows/ml-pipeline.yml`

Fichiers qui **NE DOIVENT PAS être** ajoutés:
- - `data/iris.csv` (données réelles)
- - `data/processed/` (données générées)
- - `model.pkl` (modèle entraîné)
- - `mlruns/` (runs MLflow)
- - `.venv/` (environnement virtuel)

### Étape 1.5: Faire le premier commit

```bash
git commit -m "Initial commit: MLOps project with DVC and MLflow"
```

### Étape 1.6: Lier le dépôt local au dépôt distant GitHub

```bash
# Ajouter le remote origin
git remote add origin https://github.com/AhmedBen98/mlops.git

# Vérifier le remote
git remote -v
```

### Étape 1.7: Pousser le code vers GitHub

```bash
# Renommer la branche en 'main' si nécessaire
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

**Vérification**: Allez sur https://github.com/AhmedBen98/mlops et vérifiez que tous vos fichiers sont présents.

---

## Partie 2: Configuration GitHub Actions

### Étape 2.1: Comprendre la structure du workflow

Le fichier workflow créé (`.github/workflows/ml-pipeline.yml`) contient:

1. **Trigger**: Exécution sur chaque `push` et `pull_request`
2. **Job**: `ml-pipeline` qui s'exécute sur Ubuntu
3. **Steps**:
   - Checkout du code
   - Configuration de Python
   - Installation des dépendances
   - Configuration DVC
   - Exécution du pipeline DVC
   - Entraînement du modèle
   - Évaluation et validation
   - Upload des artefacts (modèle, métriques, runs MLflow)

### Étape 2.2: Structure du fichier de workflow

Le fichier `.github/workflows/ml-pipeline.yml` a été créé avec la structure suivante:

```yaml
name: ML Pipeline CI/CD

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  ml-pipeline:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python
      - Install dependencies
      - Configure DVC
      - Run DVC pipeline
      - Train model
      - Evaluate model
      - Upload artifacts
```

### Étape 2.3: Détail des étapes du workflow

#### 1. **Checkout code**
```yaml
- name: Checkout code
  uses: actions/checkout@v3
  with:
    fetch-depth: 0  # Nécessaire pour DVC
```
- Récupère le code du dépôt
- `fetch-depth: 0` permet d'avoir l'historique complet (requis par DVC)

#### 2. **Set up Python**
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.10'
```
- Installe Python 3.10 sur le runner GitHub

#### 3. **Cache dependencies**
```yaml
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```
- Accélère l'exécution en cachant les packages Python

#### 4. **Install dependencies**
```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install dvc
```
- Installe toutes les dépendances Python nécessaires

#### 5. **Run DVC pipeline**
```yaml
- name: Run DVC pipeline
  run: dvc repro
```
- Exécute le pipeline DVC complet (preprocess + train)

#### 6. **Evaluate model**
- Calcule les métriques: accuracy, precision, recall, F1-score
- Valide que l'accuracy est ≥ 85%
- Sauvegarde les métriques dans `metrics.json`

#### 7. **Upload artifacts**
- Upload du modèle entraîné (`model.pkl`)
- Upload des métriques (`metrics.json`)
- Upload des runs MLflow (`mlruns/`)

### Étape 2.4: Configuration DVC Remote (Optionnel mais recommandé)

Pour partager les données entre les exécutions CI/CD, vous devez configurer un DVC remote.

**Option 1: Google Drive**

```bash
# Localement
dvc remote add -d storage gdrive://your-folder-id
git add .dvc/config
git commit -m "Add DVC remote storage"
git push
```

Puis dans GitHub:
1. Allez dans **Settings** > **Secrets and variables** > **Actions**
2. Ajoutez `GDRIVE_CREDENTIALS_DATA` avec vos credentials

**Option 2: AWS S3**

```bash
dvc remote add -d storage s3://my-bucket/mlops-data
dvc remote modify storage region us-east-1
```

Dans GitHub Secrets, ajoutez:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

**Option 3: Azure Blob Storage**

```bash
dvc remote add -d storage azure://mycontainer/mlops
dvc remote modify storage account_name myaccount
```

Dans GitHub Secrets, ajoutez:
- `AZURE_STORAGE_ACCOUNT`
- `AZURE_STORAGE_KEY`

**Option 4: Sans remote (pour tests)**

Si vous n'avez pas de remote storage, le workflow fonctionnera quand même car:
- Les données sont régénérées par `generate_iris.py`
- Le dataset Iris est petit et peut être commité

### Étape 2.5: Activer GitHub Actions

1. Allez sur https://github.com/AhmedBen98/mlops
2. Cliquez sur l'onglet **"Actions"**
3. Si c'est votre premier workflow, cliquez sur **"I understand my workflows, go ahead and enable them"**
4. GitHub Actions est maintenant activé!

---

## Partie 3: Test et validation du pipeline

### Étape 3.1: Modifier le dataset ou le code

Pour tester le pipeline automatique, faites une modification:

**Option A: Modifier le code du modèle**

```bash
# Modifier train.py pour changer un hyperparamètre
# Par exemple, changer n_estimators dans RandomForestClassifier
```

Exemple de modification dans `train.py`:
```python
# Avant
model = RandomForestClassifier(random_state=42)

# Après
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
```

**Option B: Modifier le dataset**

```bash
# Modifier generate_iris.py pour ajouter plus de samples
# Ou modifier data/iris.csv directement
```

**Option C: Modifier les paramètres DVC**

Modifiez `dvc.yaml` pour ajouter de nouveaux paramètres.

### Étape 3.2: Commit et push des changements

```bash
# Vérifier les modifications
git status

# Ajouter les fichiers modifiés
git add train.py  # ou les fichiers que vous avez modifiés

# Commit avec un message descriptif
git commit -m "Update model hyperparameters: n_estimators=200, max_depth=10"

# Pousser vers GitHub
git push origin main
```

### Étape 3.3: Observer l'exécution automatique

1. Allez sur https://github.com/AhmedBen98/mlops/actions
2. Vous verrez une nouvelle exécution du workflow qui démarre automatiquement
3. Cliquez sur l'exécution pour voir les détails

**Étapes visibles dans l'interface**:
- - Checkout code
- - Set up Python
- - Install dependencies
- - Run DVC pipeline
- - Train model
- - Evaluate model
- - Upload artifacts

### Étape 3.4: Vérifier les logs

Dans chaque étape, vous pouvez:
1. Cliquer sur l'étape pour voir les logs détaillés
2. Vérifier que tout s'exécute correctement
3. En cas d'erreur, les logs vous indiqueront où est le problème

**Exemple de logs attendus**:

```
Run DVC pipeline:
  Running stage 'preprocess'
  Running stage 'train'
  Model trained and saved as model.pkl

Evaluate model:
  ==================================================
  MODEL EVALUATION RESULTS
  ==================================================
  Accuracy:  0.9667
  Precision: 0.9722
  Recall:    0.9667
  F1 Score:  0.9662
  ==================================================
  SUCCESS: Model passed validation!
```

### Étape 3.5: Télécharger les artefacts

Après l'exécution:
1. Allez dans l'onglet **"Summary"** de l'exécution
2. Scrollez vers le bas jusqu'à **"Artifacts"**
3. Téléchargez:
   - `trained-model`: Le modèle entraîné
   - `metrics`: Les métriques d'évaluation
   - `mlflow-runs`: Les runs MLflow

---

## Partie 4: Traçabilité avec MLflow

### Étape 4.1: Améliorer train.py pour le tracking MLflow

Pour une meilleure traçabilité, modifiez `train.py`:

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import pickle
import os
import mlflow
import mlflow.sklearn

# Configuration MLflow
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("iris_classification")

# Démarrer un run MLflow
with mlflow.start_run():
    # Load the dataset
    data = pd.read_csv("data/iris.csv")
    X = data.drop("species", axis=1)
    y = data["species"]
    
    # Log dataset info
    mlflow.log_param("dataset_size", len(data))
    mlflow.log_param("n_features", X.shape[1])
    
    # Split the dataset
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    mlflow.log_param("test_size", test_size)
    
    # Hyperparameters
    n_estimators = 200
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    # Train the model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Save the model locally
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("Model trained and saved")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"MLflow Run ID: {mlflow.active_run().info.run_id}")
    
    # Ensure the output directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Generate the preprocessed file
    data.to_csv("data/processed/preprocessed.csv", index=False)
```

### Étape 4.2: Visualiser les runs MLflow localement

Après avoir téléchargé les artefacts `mlflow-runs`:

```bash
# Extraire l'archive
unzip mlflow-runs.zip

# Lancer l'interface MLflow
mlflow ui --backend-store-uri file:./mlruns

# Ouvrir http://localhost:5000 dans votre navigateur
```

### Étape 4.3: Comparer les métriques entre exécutions

Dans l'interface MLflow:

1. **Vue des expérimentations**:
   - Allez dans l'expérience "iris_classification"
   - Vous verrez tous les runs avec leurs métriques

2. **Comparer les runs**:
   - Sélectionnez plusieurs runs (checkbox)
   - Cliquez sur **"Compare"**
   - Visualisez les différences de métriques

3. **Graphiques**:
   - Créez des graphiques pour visualiser l'évolution:
     - Accuracy vs Time
     - Precision vs n_estimators
     - F1-score vs max_depth

### Étape 4.4: Vérifier la création automatique des runs

**Test**:
1. Faites 3 modifications différentes (ex: changez n_estimators à 100, 200, 300)
2. Poussez chaque modification séparément
3. Téléchargez les artefacts MLflow après chaque exécution
4. Comparez les 3 runs dans MLflow UI

**Résultat attendu**:
- 3 nouveaux runs dans MLflow
- Chaque run a des hyperparamètres différents
- Les métriques varient selon les hyperparamètres

---

## Résolution des problèmes courants

### Problème 1: Le workflow ne se déclenche pas

**Cause**: La branche n'est pas `main` ou `master`

**Solution**:
```bash
# Vérifier le nom de la branche
git branch

# Renommer si nécessaire
git branch -M main
```

### Problème 2: Erreur "Permission denied" dans GitHub Actions

**Cause**: Les permissions GitHub Actions ne sont pas configurées

**Solution**:
1. Allez dans **Settings** > **Actions** > **General**
2. Sous "Workflow permissions", sélectionnez **"Read and write permissions"**
3. Cliquez sur **"Save"**

### Problème 3: DVC ne trouve pas les données

**Cause**: Pas de remote DVC configuré

**Solution**:
```bash
# Option 1: Commiter les données (si petites)
git add data/iris.csv
git commit -m "Add iris dataset"

# Option 2: Configurer un remote DVC (recommandé)
dvc remote add -d storage s3://my-bucket/data
dvc push
```

### Problème 4: Le modèle échoue la validation (accuracy < 85%)

**Cause**: Hyperparamètres mal configurés ou données corrompues

**Solution**:
1. Vérifiez les hyperparamètres dans `train.py`
2. Vérifiez l'intégrité des données
3. Ajustez le seuil de validation dans le workflow si nécessaire

### Problème 5: Erreur "Module not found" dans le CI

**Cause**: Dépendance manquante dans `requirements.txt`

**Solution**:
```bash
# Mettre à jour requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Problème 6: Les artefacts ne sont pas uploadés

**Cause**: Le chemin du fichier est incorrect

**Solution**: Vérifiez que les fichiers existent:
```yaml
- name: Check files
  run: |
    ls -la
    ls -la mlruns/
```

---

## Conclusion

### Récapitulatif des étapes réalisées

- **Partie 1**: Préparation du dépôt GitHub
- Dépôt créé: https://github.com/AhmedBen98/mlops.git
- Code et fichiers DVC poussés

- **Partie 2**: Configuration GitHub Actions
- Workflow créé: `.github/workflows/ml-pipeline.yml`
- Pipeline CI/CD opérationnel

- **Partie 3**: Test et validation
- Pipeline s'exécute automatiquement sur chaque push
- Artefacts générés et téléchargeables

- **Partie 4**: Traçabilité MLflow
- Runs MLflow créés automatiquement
- Métriques comparables entre exécutions

### Bonnes pratiques CI/CD pour MLOps

1. **Versioning**:
   - - Code versionné avec Git
   - - Données versionnées avec DVC
   - - Modèles versionnés avec MLflow

2. **Automatisation**:
   - - Tests automatiques sur chaque commit
   - - Entraînement automatique du modèle
   - - Validation automatique des performances

3. **Traçabilité**:
   - - Logs détaillés dans GitHub Actions
   - - Métriques trackées dans MLflow
   - - Artefacts sauvegardés et téléchargeables

4. **Reproductibilité**:
   - - Environnement Python fixé
   - - Random seed fixé
   - - Pipeline DVC reproductible

### Améliorations futures possibles

1. **Tests unitaires**: Ajouter des tests pour le code
2. **Tests de régression**: Comparer avec le modèle précédent
3. **Déploiement automatique**: Déployer le modèle si validation OK
4. **Notifications**: Slack/Email en cas d'échec
5. **Staging environment**: Tester avant production
6. **Model registry**: Enregistrer les meilleurs modèles

### Ressources utiles

- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation DVC](https://dvc.org/doc)
- [Documentation MLflow](https://mlflow.org/docs/latest/index.html)
- [MLOps Best Practices](https://ml-ops.org/)

---

**Fin du document**

Pour toute question ou amélioration, n'hésitez pas à créer une issue sur le dépôt GitHub.
