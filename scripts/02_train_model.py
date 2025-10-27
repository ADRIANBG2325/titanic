"""
Script de Entrenamiento del Modelo - Random Forest Classifier
Entrena un modelo de Machine Learning para predecir supervivencia en el Titanic
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import pickle
import json

print("=" * 60)
print("ENTRENAMIENTO DEL MODELO - RANDOM FOREST")
print("=" * 60)

# Cargar datos
print("\n📂 Cargando datos...")
train_df = pd.read_csv('train.csv')

# Función de limpieza y preparación de datos
def prepare_data(df):
    """Limpia y prepara los datos para el modelo con ingeniería de características avanzada"""
    df = df.copy()
    
    # Rellenar valores nulos
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    # Agrupar títulos raros en 'Rare'
    rare_titles = ['Dr', 'Rev', 'Col', 'Major', 'Capt', 'Jonkheer', 'Don', 'Sir', 
                   'Lady', 'Countess', 'Dona', 'Mme', 'Mlle', 'Ms']
    df['Title'] = df['Title'].replace(rare_titles, 'Rare')
    
    df['Deck'] = df['Cabin'].str[0]
    df['Deck'].fillna('U', inplace=True)  # U = Unknown
    
    df['Age_Group'] = pd.cut(df['Age'], 
                              bins=[0, 16, 30, 50, 100], 
                              labels=['0-16', '17-30', '31-50', '51+'])
    
    # Crear feature de tamaño de familia
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    
    # Crear feature de si viaja solo
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    
    df = pd.get_dummies(df, columns=['Sex', 'Embarked', 'Title', 'Deck', 'Age_Group'], 
                        drop_first=False)
    
    return df

print("🧹 Limpiando y preparando datos con ingeniería de características avanzada...")
train_df = prepare_data(train_df)

# Excluir columnas que no son features
exclude_cols = ['PassengerId', 'Survived', 'Name', 'Ticket', 'Cabin', 'Age']
features = [col for col in train_df.columns if col not in exclude_cols]

X = train_df[features]
y = train_df['Survived']

print(f"\n📋 Features utilizadas ({len(features)}):")
for i, feature in enumerate(features, 1):
    print(f"  {i}. {feature}")

# Dividir datos en entrenamiento y validación
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\n📊 Datos de entrenamiento: {len(X_train)} registros")
print(f"📊 Datos de validación: {len(X_val)} registros")

print("\n🌲 Entrenando modelo Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2
)
model.fit(X_train, y_train)

# Evaluar modelo
train_score = model.score(X_train, y_train)
val_score = model.score(X_val, y_val)

print("\n📈 RESULTADOS DEL MODELO")
print("-" * 60)
print(f"Precisión en entrenamiento: {train_score*100:.2f}%")
print(f"Precisión en validación: {val_score*100:.2f}%")

# Validación cruzada
print("\n🔄 Realizando validación cruzada (5-fold)...")
cv_scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"Precisión promedio (CV): {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

print("\n🔍 IMPORTANCIA DE CARACTERÍSTICAS (TOP 15)")
print("-" * 60)
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(15).iterrows():
    print(f"{row['feature']}: {row['importance']:.4f}")

# Guardar modelo
print("\n💾 Guardando modelo...")
with open('titanic_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Guardar metadata del modelo
metadata = {
    'features': features,
    'train_score': float(train_score),
    'val_score': float(val_score),
    'cv_mean': float(cv_scores.mean()),
    'cv_std': float(cv_scores.std()),
    'model_type': 'Random Forest Classifier',
    'n_estimators': 100,
    'feature_count': len(features)
}

with open('model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n" + "=" * 60)
print("✅ MODELO ENTRENADO Y GUARDADO EXITOSAMENTE")
print("=" * 60)
print("\nArchivos generados:")
print("  - titanic_model.pkl (modelo Random Forest entrenado)")
print("  - model_metadata.json (metadata del modelo)")
print(f"\n🎯 Mejora esperada: ~82-85% de precisión con Random Forest")
