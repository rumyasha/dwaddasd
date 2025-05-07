from django.shortcuts import render, redirect
from .models import Recipe, Rating, Comment, Favorite
from .services.notifications import send_meal_notification

def add_recipe(request):
    if request.method == 'POST':
        recipe = Recipe.objects.create(
            title=request.POST['title'],
            author=request.user,
            meal_type=request.POST['meal_type'],
            image=request.FILES['image']
        )
        send_meal_notification(request.user, recipe)
        return redirect('recipe_detail', recipe.id)
    return render(request, 'add_recipe.html')

def rate_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    Rating.objects.update_or_create(
        user=request.user,
        recipe=recipe,
        defaults={'score': request.POST['score']}
    )
    return redirect('recipe_detail', recipe.id)