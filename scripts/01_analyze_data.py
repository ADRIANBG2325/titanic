"""
Script de Análisis Exploratorio de Datos del Titanic
Analiza y limpia los datos antes del entrenamiento del modelo
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("ANÁLISIS EXPLORATORIO DE DATOS - TITANIC")
print("=" * 60)

# Cargar datos
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

print("\n📊 INFORMACIÓN GENERAL DEL DATASET")
print("-" * 60)
print(f"Registros de entrenamiento: {len(train_df)}")
print(f"Registros de prueba: {len(test_df)}")
print(f"\nColumnas: {list(train_df.columns)}")

# Información de supervivencia
print("\n⚓ ESTADÍSTICAS DE SUPERVIVENCIA")
print("-" * 60)
survived_count = train_df['Survived'].value_counts()
survival_rate = (survived_count[1] / len(train_df)) * 100
print(f"Sobrevivieron: {survived_count[1]} ({survival_rate:.1f}%)")
print(f"No sobrevivieron: {survived_count[0]} ({100-survival_rate:.1f}%)")

# Análisis por clase
print("\n🎫 SUPERVIVENCIA POR CLASE")
print("-" * 60)
for pclass in [1, 2, 3]:
    class_data = train_df[train_df['Pclass'] == pclass]
    survival = (class_data['Survived'].sum() / len(class_data)) * 100
    print(f"Clase {pclass}: {survival:.1f}% de supervivencia")

# Análisis por género
print("\n👥 SUPERVIVENCIA POR GÉNERO")
print("-" * 60)
for sex in ['male', 'female']:
    sex_data = train_df[train_df['Sex'] == sex]
    survival = (sex_data['Survived'].sum() / len(sex_data)) * 100
    print(f"{sex.capitalize()}: {survival:.1f}% de supervivencia")

print("\n👔 ANÁLISIS DE TÍTULOS (EXTRAÍDOS DE NOMBRES)")
print("-" * 60)
train_df['Title'] = train_df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
title_counts = train_df['Title'].value_counts()
print("Títulos encontrados:")
for title, count in title_counts.items():
    survival = train_df[train_df['Title'] == title]['Survived'].mean() * 100
    print(f"  {title}: {count} pasajeros ({survival:.1f}% supervivencia)")

print("\n🚪 ANÁLISIS DE CUBIERTAS (EXTRAÍDAS DE CABIN)")
print("-" * 60)
train_df['Deck'] = train_df['Cabin'].str[0]
train_df['Deck'].fillna('U', inplace=True)
deck_counts = train_df['Deck'].value_counts()
print("Cubiertas encontradas:")
for deck, count in deck_counts.items():
    survival = train_df[train_df['Deck'] == deck]['Survived'].mean() * 100
    deck_name = 'Desconocida' if deck == 'U' else f'Cubierta {deck}'
    print(f"  {deck_name}: {count} pasajeros ({survival:.1f}% supervivencia)")

print("\n📅 ANÁLISIS DE GRUPOS DE EDAD")
print("-" * 60)
train_df['Age_Group'] = pd.cut(train_df['Age'], 
                                bins=[0, 16, 30, 50, 100], 
                                labels=['0-16', '17-30', '31-50', '51+'])
age_group_counts = train_df['Age_Group'].value_counts().sort_index()
print("Grupos de edad:")
for age_group, count in age_group_counts.items():
    survival = train_df[train_df['Age_Group'] == age_group]['Survived'].mean() * 100
    print(f"  {age_group} años: {count} pasajeros ({survival:.1f}% supervivencia)")

# Valores nulos
print("\n❓ VALORES NULOS")
print("-" * 60)
null_counts = train_df.isnull().sum()
for col in null_counts[null_counts > 0].index:
    print(f"{col}: {null_counts[col]} valores nulos ({(null_counts[col]/len(train_df)*100):.1f}%)")

# Estadísticas de edad
print("\n📈 ESTADÍSTICAS DE EDAD")
print("-" * 60)
print(f"Edad promedio: {train_df['Age'].mean():.1f} años")
print(f"Edad mediana: {train_df['Age'].median():.1f} años")
print(f"Edad mínima: {train_df['Age'].min():.0f} años")
print(f"Edad máxima: {train_df['Age'].max():.0f} años")

# Estadísticas de tarifa
print("\n💰 ESTADÍSTICAS DE TARIFA")
print("-" * 60)
print(f"Tarifa promedio: ${train_df['Fare'].mean():.2f}")
print(f"Tarifa mediana: ${train_df['Fare'].median():.2f}")
print(f"Tarifa mínima: ${train_df['Fare'].min():.2f}")
print(f"Tarifa máxima: ${train_df['Fare'].max():.2f}")

# Puerto de embarque
print("\n🚢 PUERTO DE EMBARQUE")
print("-" * 60)
embarked_counts = train_df['Embarked'].value_counts()
for port, count in embarked_counts.items():
    port_name = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}.get(port, 'Desconocido')
    survival = train_df[train_df['Embarked'] == port]['Survived'].mean() * 100
    print(f"{port_name} ({port}): {count} pasajeros ({survival:.1f}% supervivencia)")

print("\n" + "=" * 60)
print("✅ ANÁLISIS COMPLETADO")
print("=" * 60)
