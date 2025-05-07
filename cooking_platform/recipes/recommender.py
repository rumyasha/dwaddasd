from django.db.models import Count, Avg
from .models import Recipe, Rating


def recommend_recipes(user, current_recipe=None, limit=6):
    if not user.is_authenticated:
        return []

    # 1. Похожие рецепты по категории
    if current_recipe and current_recipe.category:
        category_recipes = Recipe.objects.filter(
            category=current_recipe.category,
            is_published=True
        ).exclude(id=current_recipe.id).annotate(
            avg_rating=Avg('ratings__value')
        ).order_by('-avg_rating')[:limit]

        if category_recipes.count() >= limit:
            return list(category_recipes)

    # 2. Популярные рецепты (по оценкам)
    popular_recipes = Recipe.objects.filter(
        is_published=True
    ).annotate(
        avg_rating=Avg('ratings__value'),
        rating_count=Count('ratings')
    ).order_by('-avg_rating', '-rating_count')[:limit]

    return list(popular_recipes)




class RecipeRecommender:
    def __init__(self, user):
        self.user = user

    def get_recommendations(self, current_recipe=None, limit=6):
        recommendations = []

        # 1. Рекомендации на основе избранного
        if self.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.user)
            favorite_categories = Recipe.objects.filter(
                favorited_by=user_profile
            ).values_list('category', flat=True)

            if favorite_categories:
                category_recipes = Recipe.objects.filter(
                    category__in=favorite_categories
                ).exclude(
                    Q(favorited_by=user_profile) |
                    Q(pk=current_recipe.pk) if current_recipe else Q()
                ).annotate(
                    rating_count=Count('ratings')
                ).order_by('-average_rating', '-rating_count')[:limit]

                recommendations.extend(list(category_recipes))

        # 2. Популярные рецепты
        if len(recommendations) < limit:
            popular = Recipe.objects.annotate(
                rating_count=Count('ratings')
            ).order_by('-average_rating', '-rating_count')

            if current_recipe:
                popular = popular.exclude(pk=current_recipe.pk)

            popular = popular[:limit - len(recommendations)]
            recommendations.extend(list(popular))

        return recommendations[:limit]