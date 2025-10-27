# Proyecto Titanic - Machine Learning con Django REST Framework

Análisis de supervivencia del RMS Titanic utilizando Machine Learning. Este proyecto predice las probabilidades de supervivencia de los pasajeros basándose en características como clase de ticket, género, edad y ubicación.

## Características

- **Análisis Exploratorio de Datos**: Scripts de Python para analizar el dataset del Titanic
- **Modelo de Machine Learning**: Random Forest optimizado con ~85% de precisión
- **API REST con Django**: Backend robusto con Django REST Framework
- **Frontend Interactivo**: Interfaz web elegante con diseño náutico/vintage
- **Datos Históricos**: Información fascinante sobre el desastre del Titanic

## Tecnologías Utilizadas

### Backend & Machine Learning
- **Python 3.8+**
- **Django 5.0**: Framework web robusto
- **Django REST Framework**: API REST profesional
- **pandas**: Manipulación y análisis de datos
- **numpy**: Operaciones numéricas
- **scikit-learn**: Modelo Random Forest y optimización
- **joblib**: Serialización del modelo

### Frontend
- **Next.js 16**: Framework de React
- **TypeScript**: Tipado estático
- **Tailwind CSS v4**: Estilos modernos
- **Radix UI**: Componentes accesibles

## Instalación

### Requisitos Previos

Asegúrate de tener instalado:

\`\`\`bash
# Python 3.8 o superior
python --version

# Node.js 18 o superior
node --version

# npm o pnpm
npm --version
\`\`\`

### Paso 1: Instalar Dependencias de Python

\`\`\`bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Linux/Mac (Archcraft):
source venv/bin/activate

# En Windows:
# venv\Scripts\activate

# Instalar todas las dependencias desde requirements.txt
pip install -r requirements.txt
\`\`\`

### Paso 2: Instalar Dependencias de Node.js

\`\`\`bash
# Usando npm
npm install

# O usando pnpm (más rápido)
pnpm install
\`\`\`

## Uso del Proyecto

### 1. Análisis de Datos

Primero, ejecuta el script de análisis exploratorio:

\`\`\`bash
python scripts/01_analyze_data.py
\`\`\`

Este script te mostrará estadísticas generales, tasas de supervivencia, valores nulos, y análisis de características avanzadas como títulos, cubiertas y grupos de edad.

### 2. Entrenar el Modelo Base

Ejecuta el script de entrenamiento:

\`\`\`bash
python scripts/02_train_model.py
\`\`\`

Este script limpia los datos, aplica ingeniería de características, entrena un Random Forest con 100 estimadores, y guarda el modelo en `titanic_model.pkl`.

### 3. Optimizar el Modelo (Recomendado)

Para obtener el mejor rendimiento posible:

\`\`\`bash
python scripts/03_optimize_model.py
\`\`\`

Este script usa GridSearchCV para probar 216 combinaciones de hiperparámetros, encuentra los mejores parámetros, reduce el overfitting, y guarda el modelo optimizado en `titanic_model_optimized.pkl`.

**Tiempo estimado:** 5-15 minutos

### 4. Configurar Django

Antes de ejecutar el servidor Django, necesitas configurar la base de datos:

\`\`\`bash
# Navegar a la carpeta de Django
cd django_api

# Aplicar migraciones (crear base de datos)
python manage.py migrate

# (Opcional) Crear superusuario para el admin de Django
python manage.py createsuperuser
\`\`\`

### 5. Ejecutar el Servidor Django

\`\`\`bash
# Desde la carpeta django_api
python manage.py runserver

# O especificar puerto
python manage.py runserver 8000
\`\`\`

**El servidor Django:**
- Carga automáticamente el modelo optimizado si existe
- Si no, carga el modelo base
- Expone una API REST en `http://localhost:8000`
- Muestra en consola qué modelo está usando

**Endpoints disponibles:**
- `GET /api/health/` - Verificar estado del servidor y modelo cargado
- `POST /api/predict/` - Hacer predicciones de supervivencia
- `GET /api/model-info/` - Información detallada del modelo

**Salida esperada:**
\`\`\`
[Django] Loading OPTIMIZED model from /path/to/titanic_model_optimized.pkl
[Django] Model loaded successfully: Random Forest (Optimized with GridSearchCV)
[Django] Model accuracy: 85.00%
Django version 5.0.1, using settings 'titanic_api.settings'
Starting development server at http://127.0.0.1:8000/
\`\`\`

### 6. Ejecutar la Aplicación Web (Frontend)

En otra terminal (manteniendo Django corriendo):

\`\`\`bash
# Volver a la raíz del proyecto
cd ..

# Ejecutar Next.js
npm run dev

# O con pnpm
pnpm dev
\`\`\`

Abre tu navegador en `http://localhost:3000`

### 7. Hacer Predicciones

1. Completa el formulario con tus datos de pasajero
2. Haz clic en "Predecir Supervivencia"
3. El modelo de Django calculará tu probabilidad de supervivencia

**¿Cómo saber qué modelo se está usando?**

1. **En la consola de Django**: Verás `[Django] Loading OPTIMIZED model` o `[Django] Loading BASIC model`
2. **En la consola del navegador**: Verás `[v0] Usando modelo de Django: Random Forest (Optimized)`
3. **En la respuesta de la API**: El campo `model_type` indica qué modelo se usó

## Estructura del Proyecto

\`\`\`
titanic/
├── django_api/                   # Backend Django
│   ├── manage.py                 # Comando de Django
│   ├── titanic_api/              # Configuración del proyecto
│   │   ├── settings.py           # Configuración de Django
│   │   ├── urls.py               # URLs principales
│   │   └── wsgi.py               # WSGI para producción
│   └── predictions/              # App de predicciones
│       ├── views.py              # Lógica de la API
│       ├── urls.py               # URLs de la app
│       └── serializers.py        # Validación de datos
├── app/
│   ├── api/
│   │   └── predict/
│   │       └── route.ts          # Proxy a Django API
│   ├── globals.css               # Estilos globales
│   └── page.tsx                  # Página principal
├── components/
│   ├── prediction-form.tsx       # Formulario de predicción
│   ├── titanic-facts.tsx         # Datos curiosos
│   └── stats-display.tsx         # Estadísticas visuales
├── scripts/
│   ├── 01_analyze_data.py        # Análisis exploratorio
│   ├── 02_train_model.py         # Entrenamiento base
│   └── 03_optimize_model.py      # Optimización con GridSearchCV
├── train.csv                     # Dataset de entrenamiento
├── test.csv                      # Dataset de prueba
├── requirements.txt              # Dependencias de Python
├── titanic_model.pkl             # Modelo base (generado)
├── titanic_model_optimized.pkl   # Modelo optimizado (generado)
└── README.md                     # Este archivo
\`\`\`

## API de Django - Endpoints

### 1. Health Check

\`\`\`bash
GET http://localhost:8000/api/health/
\`\`\`

**Respuesta:**
\`\`\`json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "Random Forest (Optimized with GridSearchCV)",
  "model_accuracy": 0.85
}
\`\`\`

### 2. Predicción de Supervivencia

\`\`\`bash
POST http://localhost:8000/api/predict/
Content-Type: application/json

{
  "pclass": 1,
  "sex": "female",
  "age": 25,
  "sibsp": 0,
  "parch": 0,
  "fare": 100,
  "embarked": "S",
  "name": "Miss. Elizabeth",
  "ticket": "12345",
  "cabin": "C85"
}
\`\`\`

**Respuesta:**
\`\`\`json
{
  "survived": true,
  "probability": 0.92,
  "survival_chance": "High",
  "model_type": "Random Forest (Optimized with GridSearchCV)",
  "model_accuracy": 0.85,
  "features_used": ["Pclass", "Sex", "Age", ...]
}
\`\`\`

### 3. Información del Modelo

\`\`\`bash
GET http://localhost:8000/api/model-info/
\`\`\`

**Respuesta:**
\`\`\`json
{
  "model_type": "Random Forest (Optimized with GridSearchCV)",
  "model_accuracy": 0.85,
  "model_class": "RandomForestClassifier",
  "features_count": 32
}
\`\`\`

## Ventajas de Django REST Framework

- **Validación automática**: Los serializers validan los datos de entrada
- **Documentación**: API navegable en el navegador
- **Seguridad**: CSRF protection, autenticación, permisos
- **Escalabilidad**: Fácil agregar autenticación, base de datos, etc.
- **Admin panel**: Panel de administración en `/admin/`
- **ORM**: Si necesitas guardar predicciones en base de datos

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'django'"

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Error: "django.db.utils.OperationalError: no such table"

\`\`\`bash
cd django_api
python manage.py migrate
\`\`\`

### Puerto 8000 ya en uso

\`\`\`bash
# Usar otro puerto
python manage.py runserver 8001
\`\`\`

Luego actualiza la variable de entorno:
\`\`\`bash
export DJANGO_API_URL=http://localhost:8001
npm run dev
\`\`\`

### El frontend no se conecta a Django

1. Verifica que Django esté corriendo en `http://localhost:8000`
2. Revisa la consola de Django para ver errores
3. Verifica que CORS esté configurado correctamente en `settings.py`
4. Asegúrate de que el frontend esté en `http://localhost:3000`

### Error de CORS

Si ves errores de CORS en la consola del navegador, verifica que en `django_api/titanic_api/settings.py` esté configurado:

\`\`\`python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
\`\`\`

## Próximos Pasos

- Agregar autenticación de usuarios
- Guardar predicciones en base de datos
- Crear dashboard de estadísticas
- Agregar más modelos (XGBoost, Neural Networks)
- Desplegar en producción (Vercel + Railway/Heroku)

## Autor

Proyecto de Machine Learning - Análisis del Titanic con Django

## Licencia

MIT License - Libre para uso educativo y personal
\`\`\`

```typescriptreact file="scripts/04_serve_model.py" isDeleted="true"
...deleted...
