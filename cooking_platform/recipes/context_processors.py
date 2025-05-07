from .models import MealPlan
from django.utils import timezone

def meal_plan_notifications(request):
    if request.user.is_authenticated:
        today_meals = MealPlan.objects.filter(
            user=request.user,
            date=timezone.now().date()
        ).order_by('meal_type')
        return {'today_meals': today_meals}
    return {}