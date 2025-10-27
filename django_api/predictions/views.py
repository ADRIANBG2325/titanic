from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PredictionInputSerializer, PredictionOutputSerializer
import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path


# Global variable to store loaded model
_model = None
_model_metadata = None


def load_model():
    """Load the trained model (optimized or basic)"""
    global _model, _model_metadata
    
    if _model is not None:
        return _model, _model_metadata
    
    # Get the project root directory (parent of django_api)
    base_dir = Path(__file__).resolve().parent.parent.parent
    
    # Try to load optimized model first
    optimized_model_path = base_dir / 'titanic_model_optimized.pkl'
    basic_model_path = base_dir / 'titanic_model.pkl'
    
    if optimized_model_path.exists():
        print(f"[Django] Loading OPTIMIZED model from {optimized_model_path}")
        _model = joblib.load(optimized_model_path)
        
        # Try to load metadata
        metadata_path = base_dir / 'model_metadata_optimized.json'
        if metadata_path.exists():
            import json
            with open(metadata_path, 'r') as f:
                _model_metadata = json.load(f)
        
        model_type = "Random Forest (Optimized with GridSearchCV)"
        accuracy = _model_metadata.get('best_cv_score', 0.85) if _model_metadata else 0.85
        
    elif basic_model_path.exists():
        print(f"[Django] Loading BASIC model from {basic_model_path}")
        _model = joblib.load(basic_model_path)
        model_type = "Random Forest (Basic)"
        accuracy = 0.82
        
    else:
        raise FileNotFoundError(
            "No trained model found. Please run scripts/02_train_model.py or "
            "scripts/03_optimize_model.py first."
        )
    
    print(f"[Django] Model loaded successfully: {model_type}")
    print(f"[Django] Model accuracy: {accuracy:.2%}")
    
    return _model, {
        'model_type': model_type,
        'accuracy': accuracy
    }


def prepare_features(data):
    """Prepare features for prediction (same as training script)"""
    df = pd.DataFrame([data])
    
    # Extract Title from Name if provided
    if 'name' in data and data['name']:
        df['Title'] = df['name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        title_mapping = {
            'Mr': 'Mr', 'Miss': 'Miss', 'Mrs': 'Mrs', 'Master': 'Master'
        }
        df['Title'] = df['Title'].map(title_mapping).fillna('Rare')
    else:
        # Infer title from sex and age
        if data['sex'] == 'male':
            df['Title'] = 'Master' if data['age'] < 18 else 'Mr'
        else:
            df['Title'] = 'Miss' if data['age'] < 18 else 'Mrs'
    
    # Extract Deck from Cabin if provided
    if 'cabin' in data and data['cabin']:
        df['Deck'] = df['cabin'].str[0]
    else:
        df['Deck'] = 'U'  # Unknown
    
    # Create Age_Group
    if data['age'] <= 16:
        df['Age_Group'] = 'Child'
    elif data['age'] <= 30:
        df['Age_Group'] = 'Young_Adult'
    elif data['age'] <= 50:
        df['Age_Group'] = 'Adult'
    else:
        df['Age_Group'] = 'Senior'
    
    # Create FamilySize
    df['FamilySize'] = data['sibsp'] + data['parch'] + 1
    
    # Create IsAlone
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    
    # Convert Sex to numeric
    df['Sex'] = (data['sex'] == 'male').astype(int)
    
    # Select features for model
    features = pd.DataFrame({
        'Pclass': [data['pclass']],
        'Sex': [df['Sex'].iloc[0]],
        'Age': [data['age']],
        'SibSp': [data['sibsp']],
        'Parch': [data['parch']],
        'Fare': [data['fare']],
        'FamilySize': [df['FamilySize'].iloc[0]],
        'IsAlone': [df['IsAlone'].iloc[0]],
    })
    
    # One-hot encode categorical features
    embarked_dummies = pd.get_dummies(pd.Series([data['embarked']]), prefix='Embarked')
    title_dummies = pd.get_dummies(df['Title'], prefix='Title')
    deck_dummies = pd.get_dummies(df['Deck'], prefix='Deck')
    age_group_dummies = pd.get_dummies(df['Age_Group'], prefix='Age_Group')
    
    # Combine all features
    features = pd.concat([
        features.reset_index(drop=True),
        embarked_dummies.reset_index(drop=True),
        title_dummies.reset_index(drop=True),
        deck_dummies.reset_index(drop=True),
        age_group_dummies.reset_index(drop=True)
    ], axis=1)
    
    # Ensure all expected columns are present (model was trained with specific columns)
    expected_columns = [
        'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'FamilySize', 'IsAlone',
        'Embarked_C', 'Embarked_Q', 'Embarked_S',
        'Title_Master', 'Title_Miss', 'Title_Mr', 'Title_Mrs', 'Title_Rare',
        'Deck_A', 'Deck_B', 'Deck_C', 'Deck_D', 'Deck_E', 'Deck_F', 'Deck_G', 'Deck_T', 'Deck_U',
        'Age_Group_Adult', 'Age_Group_Child', 'Age_Group_Senior', 'Age_Group_Young_Adult'
    ]
    
    for col in expected_columns:
        if col not in features.columns:
            features[col] = 0
    
    # Reorder columns to match training
    features = features[expected_columns]
    
    return features


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    try:
        model, metadata = load_model()
        return Response({
            'status': 'healthy',
            'model_loaded': True,
            'model_type': metadata['model_type'],
            'model_accuracy': metadata['accuracy']
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'model_loaded': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def predict_survival(request):
    """Predict survival probability for a Titanic passenger"""
    
    # Validate input data
    serializer = PredictionInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Load model
        model, metadata = load_model()
        
        # Prepare features
        features = prepare_features(serializer.validated_data)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        # Prepare response
        survival_prob = float(probability[1])
        survived = bool(prediction)
        
        # Determine survival chance category
        if survival_prob < 0.3:
            survival_chance = "Low"
        elif survival_prob < 0.6:
            survival_chance = "Medium"
        else:
            survival_chance = "High"
        
        response_data = {
            'survived': survived,
            'probability': survival_prob,
            'survival_chance': survival_chance,
            'model_type': metadata['model_type'],
            'model_accuracy': metadata['accuracy'],
            'features_used': list(features.columns)
        }
        
        output_serializer = PredictionOutputSerializer(data=response_data)
        if output_serializer.is_valid():
            return Response(output_serializer.validated_data)
        else:
            return Response(response_data)
        
    except FileNotFoundError as e:
        return Response({
            'error': str(e),
            'message': 'Please train the model first by running the training scripts.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'An error occurred during prediction.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def model_info(request):
    """Get information about the loaded model"""
    try:
        model, metadata = load_model()
        
        return Response({
            'model_type': metadata['model_type'],
            'model_accuracy': metadata['accuracy'],
            'model_class': str(type(model).__name__),
            'features_count': model.n_features_in_ if hasattr(model, 'n_features_in_') else 'Unknown',
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
