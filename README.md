# Projet MLOps avec MLflow, DVC et CI/CD

[![CI/CD Pipeline](https://github.com/AhmedBen98/mlops/actions/workflows/ml-pipeline.yml/badge.svg)](https://github.com/AhmedBen98/mlops/actions)

##  Quick Start

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/AhmedBen98/mlops.git
cd mlops

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
pip install dvc
```

### Exécution

```bash
# Générer les données
python generate_iris.py

# Exécuter le pipeline DVC
dvc repro

# Visualiser MLflow
mlflow ui
```

##  Structure du projet

```
mlops/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml    # Pipeline CI/CD
├── data/
│   ├── iris.csv              # Dataset (tracké par DVC)
│   └── processed/            # Données prétraitées
├── train.py                  # Script d'entraînement
├── generate_iris.py          # Génération du dataset
├── dvc.yaml                  # Pipeline DVC
├── requirements.txt          # Dépendances Python
└── GUIDE_CONFIGURATION_CICD.md  # Documentation complète
```

##  Pipeline CI/CD

Le pipeline GitHub Actions s'exécute automatiquement sur chaque push et:
1. - Installe les dépendances
2. - Exécute le pipeline DVC
3. - Entraîne le modèle
4. - Valide les performances (accuracy ≥ 85%)
5. - Upload les artefacts (modèle, métriques, runs MLflow)

##  Tracking avec MLflow

Chaque exécution crée un nouveau run MLflow avec:
- Hyperparamètres (n_estimators, max_depth, etc.)
- Métriques (accuracy, precision, recall, F1-score)
- Modèle sauvegardé
- Artefacts

##  Documentation complète

Consultez [GUIDE_CONFIGURATION_CICD.md](./GUIDE_CONFIGURATION_CICD.md) pour:
- Configuration détaillée de GitHub Actions
- Étapes de configuration du CI/CD
- Tests et validation du pipeline
- Traçabilité avec MLflow
- Résolution des problèmes courants

##  Technologies utilisées

- **Python 3.10**
- **Scikit-learn**: Machine Learning
- **MLflow**: Tracking des expérimentations
- **DVC**: Versioning des données et pipelines
- **GitHub Actions**: CI/CD

---

## Explication complète du fichier `train.py`

Le fichier `train.py` met en œuvre un pipeline d'entraînement de modèle avec suivi des expériences grâce à MLflow. Voici une explication détaillée de chaque partie du code :

### 1. Importation des bibliothèques
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
import mlflow
import mlflow.sklearn
```
- **`sklearn.datasets`** : Permet de charger le jeu de données Iris.
- **`train_test_split`** : Divise les données en ensembles d'entraînement et de test.
- **`RandomForestClassifier`** : Implémente un modèle d'ensemble basé sur des arbres de décision.
- **`accuracy_score` et `precision_score`** : Calculent les métriques de performance.
- **`mlflow`** : Fournit des outils pour suivre les expériences et enregistrer les modèles.

### 2. Définition de l'expérience MLflow
```python
mlflow.set_experiment("iris-mlops")
```
- Définit ou sélectionne une expérience MLflow nommée `iris-mlops`.
- Si l'expérience n'existe pas, elle est créée automatiquement.

### 3. Boucle sur différentes valeurs de `n_estimators`
```python
for n_estimators in [10, 20, 30, 40]:
```
- Teste plusieurs configurations du modèle en variant le nombre d'estimateurs (arbres) dans la forêt aléatoire.

### 4. Chargement des données
```python
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
```
- **`load_iris`** : Charge les caractéristiques (X) et les étiquettes (y) du jeu de données Iris.
- **`train_test_split`** : Divise les données en ensembles d'entraînement et de test avec un `random_state` fixé pour garantir la reproductibilité.

### 5. Entraînement du modèle
```python
model = RandomForestClassifier(n_estimators=n_estimators, random_state=123)
model.fit(X_train, y_train)
```
- **`RandomForestClassifier`** : Crée un modèle de forêt aléatoire avec le nombre d'estimateurs spécifié.
- **`fit`** : Entraîne le modèle sur les données d'entraînement.

### 6. Prédiction et calcul des métriques
```python
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds, average='weighted')
```
- **`predict`** : Génère des prédictions sur les données de test.
- **`accuracy_score`** : Calcule la précision globale des prédictions.
- **`precision_score`** : Calcule la précision pondérée des prédictions.

### 7. Suivi des paramètres, métriques et modèle avec MLflow
```python
mlflow.log_param("n_estimators", n_estimators)
mlflow.log_metric("accuracy", acc)
mlflow.log_metric("precision", precision)
mlflow.sklearn.log_model(model, "model")
```
- **`log_param`** : Enregistre le paramètre `n_estimators`.
- **`log_metric`** : Enregistre les métriques `accuracy` et `precision`.
- **`log_model`** : Enregistre le modèle entraîné comme artefact.

### 8. Affichage des résultats
```python
print(f"n_estimators: {n_estimators}, Accuracy: {acc}, Precision: {precision}")
```
- Affiche les valeurs de `n_estimators`, `accuracy` et `precision` pour chaque configuration testée.

---

## Réponses aux questions

### Pourquoi MLflow est-il indispensable en MLOps ?
MLflow est essentiel en MLOps car il permet de :
1. **Suivi des expériences** :
   - MLflow enregistre les paramètres, métriques, modèles et artefacts, ce qui facilite la comparaison des résultats entre différentes expériences.
2. **Reproductibilité** :
   - Grâce au suivi des configurations et des dépendances, il est possible de reproduire les résultats obtenus.
3. **Gestion des modèles** :
   - MLflow permet de versionner les modèles, de les déployer et de les servir facilement.
4. **Collaboration** :
   - Les équipes peuvent partager les résultats et les modèles via une interface centralisée.
5. **Automatisation** :
   - Il s'intègre dans les pipelines CI/CD pour automatiser le déploiement des modèles.

---

### Quelle différence entre un run et un experiment ?
1. **Experiment** :
   - Un experiment est un conteneur logique qui regroupe plusieurs runs.
   - Exemple : Vous pouvez créer un experiment nommé "iris-mlops" pour tester différents modèles ou configurations sur le jeu de données Iris.

2. **Run** :
   - Un run est une exécution individuelle d'un modèle ou d'une configuration spécifique.
   - Chaque run enregistre les paramètres, métriques et artefacts associés à cette exécution.

**Relation** : Un experiment peut contenir plusieurs runs, mais un run appartient toujours à un seul experiment.

---

### Peut-on reproduire un modèle sans tracking ?
- **Sans tracking (comme MLflow)** :
  - Il est **difficile** de reproduire un modèle, car les informations critiques (paramètres, métriques, dépendances, code source) risquent de ne pas être enregistrées de manière systématique.
  - Cela peut entraîner des erreurs ou des incohérences lors de la tentative de reproduction.

- **Avec tracking (comme MLflow)** :
  - Le tracking garantit que toutes les informations nécessaires sont enregistrées, ce qui rend la reproduction fiable et systématique.

En résumé, sans tracking, la reproductibilité est possible mais laborieuse et sujette à des erreurs. Avec MLflow, elle devient simple et fiable.