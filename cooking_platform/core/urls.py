from django.urls import path
from recipes import views

urlpatterns = [
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('rate/<int:recipe_id>/', views.rate_recipe, name='rate_recipe'),
    path('add-comment/<int:recipe_id>/', views.add_comment, name='add_comment'),
    path('add-favorite/<int:recipe_id>/', views.add_favorite, name='add_favorite'),
]