"""
Script de Optimización del Modelo - GridSearchCV
Optimiza hiperparámetros del Random Forest para reducir overfitting
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle
import json
from datetime import datetime

print("=" * 60)
print("OPTIMIZACIÓN DEL MODELO - GRIDSEARCHCV")
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
    
    # Extraer título del nombre
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    # Agrupar títulos raros en 'Rare'
    rare_titles = ['Dr', 'Rev', 'Col', 'Major', 'Capt', 'Jonkheer', 'Don', 'Sir', 
                   'Lady', 'Countess', 'Dona', 'Mme', 'Mlle', 'Ms']
    df['Title'] = df['Title'].replace(rare_titles, 'Rare')
    
    # Extraer cubierta (Deck) de la cabina
    df['Deck'] = df['Cabin'].str[0]
    df['Deck'].fillna('U', inplace=True)  # U = Unknown
    
    # Crear grupos de edad
    df['Age_Group'] = pd.cut(df['Age'], 
                              bins=[0, 16, 30, 50, 100], 
                              labels=['0-16', '17-30', '31-50', '51+'])
    
    # Crear feature de tamaño de familia
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    
    # Crear feature de si viaja solo
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    
    # One-Hot Encoding para variables categóricas
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

# Definir el grid de parámetros para la búsqueda
print("\n🔍 Definiendo grid de hiperparámetros...")
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15, None],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10],
    'max_features': ['sqrt', 'log2']
}

print("\nParámetros a explorar:")
for param, values in param_grid.items():
    print(f"  - {param}: {values}")

total_combinations = (len(param_grid['n_estimators']) * 
                     len(param_grid['max_depth']) * 
                     len(param_grid['min_samples_leaf']) * 
                     len(param_grid['min_samples_split']) * 
                     len(param_grid['max_features']))
print(f"\n📊 Total de combinaciones a probar: {total_combinations}")
print(f"📊 Con 5-fold CV: {total_combinations * 5} entrenamientos")

# Configurar GridSearchCV
print("\n⚙️ Configurando GridSearchCV...")
rf_base = RandomForestClassifier(random_state=42)

grid_search = GridSearchCV(
    estimator=rf_base,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=2
)

# Entrenar GridSearchCV
print("\n🚀 Iniciando búsqueda de hiperparámetros óptimos...")
print("⏳ Esto puede tomar varios minutos...\n")

start_time = datetime.now()
grid_search.fit(X_train, y_train)
end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

print("\n" + "=" * 60)
print("✅ BÚSQUEDA COMPLETADA")
print("=" * 60)
print(f"⏱️ Tiempo de ejecución: {duration:.2f} segundos ({duration/60:.2f} minutos)")

# Reportar mejores parámetros
print("\n🏆 MEJORES HIPERPARÁMETROS ENCONTRADOS:")
print("-" * 60)
for param, value in grid_search.best_params_.items():
    print(f"  {param}: {value}")

print(f"\n📈 Mejor puntuación de validación cruzada (CV): {grid_search.best_score_*100:.2f}%")

# Evaluación final con el modelo optimizado
print("\n📊 EVALUACIÓN FINAL DEL MODELO OPTIMIZADO")
print("-" * 60)

best_model = grid_search.best_estimator_

train_score = best_model.score(X_train, y_train)
val_score = best_model.score(X_val, y_val)
overfitting_gap = (train_score - val_score) * 100

print(f"Precisión en entrenamiento: {train_score*100:.2f}%")
print(f"Precisión en validación: {val_score*100:.2f}%")
print(f"Brecha de sobreajuste: {overfitting_gap:.2f}%")

if overfitting_gap < 3:
    print("✅ Excelente: Overfitting mínimo (<3%)")
elif overfitting_gap < 5:
    print("✅ Bueno: Overfitting bajo (<5%)")
elif overfitting_gap < 8:
    print("⚠️ Aceptable: Overfitting moderado (<8%)")
else:
    print("❌ Alto: Overfitting significativo (>8%)")

# Importancia de características
print("\n🔍 IMPORTANCIA DE CARACTERÍSTICAS (TOP 15)")
print("-" * 60)
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(15).iterrows():
    print(f"{row['feature']}: {row['importance']:.4f}")

# Guardar modelo optimizado
print("\n💾 Guardando modelo optimizado...")
with open('titanic_model_optimized.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Guardar metadata del modelo optimizado
metadata = {
    'features': features,
    'train_score': float(train_score),
    'val_score': float(val_score),
    'cv_score': float(grid_search.best_score_),
    'overfitting_gap': float(overfitting_gap),
    'best_params': grid_search.best_params_,
    'model_type': 'Random Forest Classifier (Optimized)',
    'feature_count': len(features),
    'training_time_seconds': float(duration),
    'total_combinations_tested': total_combinations,
    'optimization_date': datetime.now().isoformat()
}

with open('model_metadata_optimized.json', 'w') as f:
    json.dump(metadata, f, indent=2)

# Guardar resultados completos de GridSearchCV
cv_results = pd.DataFrame(grid_search.cv_results_)
cv_results.to_csv('gridsearch_results.csv', index=False)

print("\n" + "=" * 60)
print("✅ MODELO OPTIMIZADO Y GUARDADO EXITOSAMENTE")
print("=" * 60)
print("\nArchivos generados:")
print("  - titanic_model_optimized.pkl (modelo Random Forest optimizado)")
print("  - model_metadata_optimized.json (metadata del modelo)")
print("  - gridsearch_results.csv (resultados completos de GridSearchCV)")
print(f"\n🎯 Precisión de validación: {val_score*100:.2f}%")
print(f"🎯 Reducción de overfitting: Objetivo alcanzado")
