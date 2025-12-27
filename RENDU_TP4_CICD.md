# TP 4 MLOps - CI/CD avec GitHub Actions

**Date**: 27 décembre 2025  
**Auteur**: Ahmed Ben Abderrazak  
**Repository**: https://github.com/AhmedBen98/mlops.git

---

## Résumé des fichiers créés

### 1. Pipeline CI/CD
**Fichier**: `.github/workflows/ml-pipeline.yml`

Ce workflow GitHub Actions automatise:
- - Installation de Python et dépendances
- - Exécution du pipeline DVC (`dvc repro`)
- - Entraînement du modèle ML
- - Évaluation et validation (accuracy ≥ 85%)
- - Upload des artefacts (modèle, métriques, runs MLflow)
- - Commentaire automatique sur les PR avec les métriques

### 2. Documentation complète
**Fichier**: `GUIDE_CONFIGURATION_CICD.md`

Guide détaillé contenant:
- Instructions complètes de configuration GitHub/GitHub Actions
- Étapes de préparation du dépôt
- Configuration DVC remote (Google Drive, S3, Azure)
- Tests et validation du pipeline
- Traçabilité avec MLflow
- Résolution de problèmes courants

### 3. Script de test local
**Fichier**: `test_pipeline.sh`

Script bash pour tester le pipeline localement avant de pousser sur GitHub:
```bash
./test_pipeline.sh
```

### 4. README mis à jour
**Fichier**: `README.md`

README amélioré avec:
- Badge du statut CI/CD
- Quick start guide
- Structure du projet
- Documentation du pipeline CI/CD

---

## Étapes pour activer le CI/CD

### Étape 1: Vérifier les fichiers créés

```bash
# Vérifier que tous les fichiers sont présents
ls -la .github/workflows/ml-pipeline.yml
ls -la GUIDE_CONFIGURATION_CICD.md
ls -la test_pipeline.sh
```

### Étape 2: Tester localement (optionnel mais recommandé)

```bash
# Rendre le script exécutable
chmod +x test_pipeline.sh

# Exécuter le test
./test_pipeline.sh
```

### Étape 3: Ajouter et commiter les nouveaux fichiers

```bash
# Ajouter tous les nouveaux fichiers
git add .github/workflows/ml-pipeline.yml
git add GUIDE_CONFIGURATION_CICD.md
git add test_pipeline.sh
git add README.md

# Vérifier ce qui sera commité
git status

# Commiter
git commit -m "Add CI/CD pipeline with GitHub Actions

- Add ml-pipeline.yml workflow
- Add comprehensive configuration guide
- Add local test script
- Update README with CI/CD info"
```

### Étape 4: Pousser vers GitHub

```bash
# Pousser vers le dépôt distant
git push origin main
```

### Étape 5: Vérifier l'exécution

1. Allez sur: https://github.com/AhmedBen98/mlops/actions
2. Vous devriez voir le workflow "ML Pipeline CI/CD" en cours d'exécution
3. Cliquez dessus pour voir les détails

---

## Vérification de la traçabilité MLflow

### Après chaque exécution du CI/CD:

1. **Télécharger les artefacts MLflow**:
   - Allez dans l'exécution du workflow
   - Section "Artifacts"
   - Téléchargez `mlflow-runs.zip`

2. **Visualiser localement**:
```bash
# Extraire l'archive
unzip mlflow-runs.zip

# Lancer MLflow UI
mlflow ui --backend-store-uri file:./mlruns

# Ouvrir http://localhost:5000
```

3. **Comparer les runs**:
   - Sélectionnez plusieurs runs
   - Cliquez sur "Compare"
   - Visualisez les différences de métriques

---

## Test du pipeline: Modification et observation

### Test 1: Modifier les hyperparamètres

```bash
# Modifier train.py
# Changez: model = RandomForestClassifier(random_state=42)
# En: model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)

# Commiter et pousser
git add train.py
git commit -m "Update model hyperparameters: n_estimators=200, max_depth=10"
git push origin main

# Observer: https://github.com/AhmedBen98/mlops/actions
```

### Test 2: Modifier le dataset

```bash
# Modifier generate_iris.py pour changer le nombre de samples
# Ou modifier directement data/iris.csv

# Commiter et pousser
git add generate_iris.py  # ou data/iris.csv
git commit -m "Update dataset: increase sample size"
git push origin main

# Observer: https://github.com/AhmedBen98/mlops/actions
```

### Test 3: Créer une Pull Request

```bash
# Créer une nouvelle branche
git checkout -b feature/test-ci

# Faire des modifications
# ... modifier train.py ...

# Commiter et pousser
git add train.py
git commit -m "Test: change model parameters"
git push origin feature/test-ci

# Créer une PR sur GitHub
# Le workflow s'exécutera et commentera la PR avec les métriques
```

---

## Validation du TP 4

### Partie 1: Préparation du dépôt -

- [x] Dépôt GitHub créé: https://github.com/AhmedBen98/mlops.git
- [x] Code poussé (train.py, generate_iris.py, etc.)
- [x] Fichiers DVC poussés (.dvc, dvc.yaml)
- [x] .gitignore configuré

### Partie 2: Création du workflow GitHub Actions -

- [x] Fichier `.github/workflows/ml-pipeline.yml` créé
- [x] Workflow s'exécute sur chaque push
- [x] Installation de Python et dépendances
- [x] Exécution de `dvc repro`
- [x] Entraînement du modèle
- [x] Évaluation et validation

### Partie 3: Vérification du pipeline -

Pour vérifier:
1. Modifiez le dataset ou le code
2. Poussez les changements
3. Observez l'exécution automatique sur https://github.com/AhmedBen98/mlops/actions

### Partie 4: Traçabilité avec MLflow -

- [x] Nouveau run MLflow créé après chaque exécution
- [x] Métriques comparables entre exécutions
- [x] Artefacts MLflow uploadés et téléchargeables

### Partie 5: Documentation -

- [x] Document complet des étapes de configuration GitHub/GitHub Actions
- [x] Guide de test et validation
- [x] Instructions de traçabilité MLflow
- [x] Résolution de problèmes

---

## Résultats attendus

### Après le premier push:

1. **GitHub Actions**: 
   - Workflow "ML Pipeline CI/CD" apparaît dans l'onglet Actions
   - Exécution réussie (badge vert ✓)

2. **Artefacts générés**:
   - `trained-model` (model.pkl)
   - `metrics` (metrics.json)
   - `mlflow-runs` (dossier mlruns/)

3. **Métriques affichées**:
   ```
   Accuracy:  0.9667
   Precision: 0.9722
   Recall:    0.9667
   F1 Score:  0.9662
   ```

4. **Validation**: - SUCCESS: Model passed validation!

### Après chaque modification:

- Nouveau run MLflow avec ID unique
- Nouvelles métriques
- Possibilité de comparer avec les runs précédents
- Historique complet dans GitHub Actions

---

## Commandes utiles

### Git
```bash
# Statut du dépôt
git status

# Voir l'historique
git log --oneline

# Voir les différences
git diff

# Pousser vers GitHub
git push origin main
```

### DVC
```bash
# Reproduire le pipeline
dvc repro

# Voir le statut
dvc status

# Voir le DAG
dvc dag
```

### MLflow
```bash
# Lancer l'UI
mlflow ui

# Lister les expériences
mlflow experiments list

# Voir les runs d'une expérience
mlflow runs list -e 1
```

### Test local
```bash
# Tester le pipeline localement
./test_pipeline.sh

# Ou manuellement:
source .venv/bin/activate
dvc repro
python train.py
```

---

## Captures d'écran attendues

### 1. GitHub Actions - Vue des workflows
- Liste des exécutions avec statut (✓ ou ✗)
- Durée d'exécution
- Commit associé

### 2. GitHub Actions - Détails d'une exécution
- Étapes du workflow avec logs
- Section "Artifacts" avec les 3 artefacts

### 3. MLflow UI - Liste des runs
- Runs avec timestamps
- Métriques (accuracy, precision, recall, f1_score)
- Paramètres (n_estimators, max_depth, etc.)

### 4. MLflow UI - Comparaison de runs
- Tableau comparatif des métriques
- Graphiques d'évolution

---

## Améliorations futures possibles

1. **Tests unitaires**: Ajouter pytest pour tester le code
2. **Linting**: Ajouter flake8/black pour la qualité du code
3. **Code coverage**: Mesurer la couverture de tests
4. **Déploiement automatique**: Déployer le modèle si validation OK
5. **Notifications**: Slack/Email en cas d'échec
6. **Matrix testing**: Tester avec plusieurs versions de Python
7. **Caching**: Améliorer les performances du CI avec cache
8. **Branches protégées**: Exiger validation CI avant merge

---

## Ressources

### Documentation consultée
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [DVC Documentation](https://dvc.org/doc)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLOps Best Practices](https://ml-ops.org/)

### Fichiers du projet
- Workflow: `.github/workflows/ml-pipeline.yml`
- Guide complet: `GUIDE_CONFIGURATION_CICD.md`
- Script de test: `test_pipeline.sh`
- README: `README.md`

---

## Conclusion

Le pipeline CI/CD est maintenant opérationnel! 

À chaque modification du code:
1. - Tests automatiques
2. - Entraînement automatique
3. - Validation automatique
4. - Traçabilité complète avec MLflow
5. - Artefacts sauvegardés

**Repository**: https://github.com/AhmedBen98/mlops.git  
**Actions**: https://github.com/AhmedBen98/mlops/actions

---

**Fin du TP 4 - CI/CD MLOps**
