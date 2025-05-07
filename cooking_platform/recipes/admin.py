from django.contrib import admin
from apps.recipes.models import *


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'cooking_time', 'difficulty', 'created_at')
    list_display_links = ('title', 'author')
    list_filter = ('difficulty', 'cuisine_type', 'created_at')
    search_fields = ('title', 'ingredients', 'instructions')
    ordering = ('-created_at', 'title')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'author', 'description')
        }),
        ('Детали рецепта', {
            'fields': ('ingredients', 'instructions', 'cooking_time', 'servings')
        }),
        ('Классификация', {
            'fields': ('cuisine_type', 'meal_type', 'difficulty', 'tags')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at', 'image')
        }),
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(CuisineType)
class CuisineTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'recipe_count')
    list_display_links = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'bio')

    def recipe_count(self, obj):
        return obj.recipes.count()

    recipe_count.short_description = 'Количество рецептов'


admin.site.register(MealType)
admin.site.register(RecipeRating)