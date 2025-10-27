from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('predict/', views.predict_survival, name='predict_survival'),
    path('model-info/', views.model_info, name='model_info'),
]
