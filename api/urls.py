from django.urls import path
from . import views

urlpatterns = [
    path('meal/', views.meal_data, name='meal_data'),
    path('nutrition/', views.nutrition_summary, name='nutrition_summary'),
    path('suggestions/', views.suggestions, name='suggestions'),
]
