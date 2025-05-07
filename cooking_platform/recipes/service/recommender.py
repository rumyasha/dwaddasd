from django.db.models import Count

def get_recommendations(user):
    # Простейшая рекомендация по типу еды
    return Recipe.objects.annotate(
        rating_count=Count('ratings')
    ).order_by('-rating_count')[:5]