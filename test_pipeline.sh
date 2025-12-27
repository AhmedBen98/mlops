#!/bin/bash

# Script pour tester le pipeline CI/CD localement avant de pousser sur GitHub

echo "=========================================="
echo "Test du Pipeline MLOps CI/CD"
echo "=========================================="
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Vérifier Python
echo -e "${YELLOW}[1/7] Vérification de Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python trouvé: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python non trouvé${NC}"
    exit 1
fi
echo ""

# 2. Vérifier l'environnement virtuel
echo -e "${YELLOW}[2/7] Vérification de l'environnement virtuel...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓ Environnement virtuel trouvé${NC}"
    source .venv/bin/activate
else
    echo -e "${RED}✗ Environnement virtuel non trouvé. Création...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    echo -e "${GREEN}✓ Environnement virtuel créé${NC}"
fi
echo ""

# 3. Installer les dépendances
echo -e "${YELLOW}[3/7] Installation des dépendances...${NC}"
pip install -q -r requirements.txt
pip install -q dvc
echo -e "${GREEN}✓ Dépendances installées${NC}"
echo ""

# 4. Vérifier DVC
echo -e "${YELLOW}[4/7] Vérification de DVC...${NC}"
if [ -f "dvc.yaml" ]; then
    echo -e "${GREEN}✓ dvc.yaml trouvé${NC}"
else
    echo -e "${RED}✗ dvc.yaml non trouvé${NC}"
    exit 1
fi
echo ""

# 5. Exécuter le pipeline DVC
echo -e "${YELLOW}[5/7] Exécution du pipeline DVC...${NC}"
dvc repro
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pipeline DVC exécuté avec succès${NC}"
else
    echo -e "${RED}✗ Erreur lors de l'exécution du pipeline DVC${NC}"
    exit 1
fi
echo ""

# 6. Entraîner le modèle
echo -e "${YELLOW}[6/7] Entraînement du modèle...${NC}"
python train.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Modèle entraîné avec succès${NC}"
else
    echo -e "${RED}✗ Erreur lors de l'entraînement${NC}"
    exit 1
fi
echo ""

# 7. Évaluation du modèle
echo -e "${YELLOW}[7/7] Évaluation du modèle...${NC}"
python -c "
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load data
data = pd.read_csv('data/iris.csv')
X = data.drop('species', axis=1)
y = data['species']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Predictions
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Display metrics
print('=' * 50)
print('MODEL EVALUATION RESULTS')
print('=' * 50)
print(f'Accuracy:  {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall:    {recall:.4f}')
print(f'F1 Score:  {f1:.4f}')
print('=' * 50)

# Save metrics
metrics = {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1_score': f1
}

with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

# Validation
if accuracy < 0.85:
    print('WARNING: Model accuracy below threshold (0.85)')
    exit(1)
else:
    print('SUCCESS: Model passed validation!')
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Évaluation réussie${NC}"
else
    echo -e "${RED}✗ Échec de la validation${NC}"
    exit 1
fi
echo ""

# Résumé
echo "=========================================="
echo -e "${GREEN}✓ Tous les tests ont réussi!${NC}"
echo "=========================================="
echo ""
echo "Le pipeline est prêt à être poussé sur GitHub."
echo ""
echo "Prochaines étapes:"
echo "  1. git add ."
echo "  2. git commit -m 'Votre message'"
echo "  3. git push origin main"
echo ""
echo "Le workflow GitHub Actions s'exécutera automatiquement!"
echo "Consultez: https://github.com/AhmedBen98/mlops/actions"
