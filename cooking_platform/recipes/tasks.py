from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
import requests
from .models import MealPlan, Notification
from datetime import date, timedelta


@shared_task
def send_meal_plan_reminders():
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Уведомления на сегодня
    send_daily_reminders(today)

    # Уведомления на завтра (утром)
    send_daily_reminders(tomorrow, is_tomorrow=True)


def send_daily_reminders(day, is_tomorrow=False):
    users = MealPlan.objects.filter(
        date=day
    ).values_list('user', flat=True).distinct()

    for user_id in users:
        send_user_reminder(user_id, day, is_tomorrow)


def send_user_reminder(user_id, day, is_tomorrow):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
        meal_plans = MealPlan.objects.filter(user=user, date=day)

        if not meal_plans.exists():
            return

        # Email уведомление
        if user.receive_email_notifications:
            send_email_reminder(user, meal_plans, day, is_tomorrow)

        # Telegram уведомление
        if user.receive_telegram_notifications and user.telegram_chat_id:
            send_telegram_reminder(user, meal_plans, day, is_tomorrow)

        # Внутреннее уведомление
        create_in_app_notification(user, meal_plans, day, is_tomorrow)

    except User.DoesNotExist:
        pass


def send_email_reminder(user, meal_plans, day, is_tomorrow):
    subject = f"Ваш план питания на {'завтра' if is_tomorrow else 'сегодня'}"

    message = render_to_string('recipes/email/meal_plan_reminder.html', {
        'user': user,
        'meal_plans': meal_plans,
        'day': day,
        'is_tomorrow': is_tomorrow,
        'site_url': settings.SITE_URL
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
        fail_silently=True
    )


def send_telegram_reminder(user, meal_plans, day, is_tomorrow):
    import telegram
    from telegram import ParseMode

    try:
        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        message = f"🍽 *План питания на {day.strftime('%d.%m.%Y')}*\n\n"

        for plan in meal_plans:
            message += (
                f"*{plan.get_meal_type_display()}*: "
                f"[{plan.recipe.title}]({settings.SITE_URL}/recipes/{plan.recipe.slug}/)\n"
            )

        bot.send_message(
            chat_id=user.telegram_chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")


def create_in_app_notification(user, meal_plans, day, is_tomorrow):
    message = f"У вас запланировано {meal_plans.count()} рецептов на {day.strftime('%d.%m.%Y')}"

    Notification.objects.create(
        user=user,
        message=message,
        notification_type='meal_reminder',
        related_recipe=meal_plans.first().recipe if meal_plans.exists() else None
    )