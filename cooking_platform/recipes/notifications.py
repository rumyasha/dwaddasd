import requests
from django.core.mail import send_mail
from django.conf import settings


def send_meal_notification(user, recipe):
    # Отправка на email
    send_mail(
        f'Рецепт на {recipe.get_meal_type_display()}',
        f'Попробуйте: {recipe.title}',
        settings.EMAIL_HOST_USER,
        [user.email]
    )

    # Отправка в Telegram
    if hasattr(user, 'telegram_chat_id'):
        message = f"🍽 {recipe.get_meal_type_display()}: {recipe.title}"
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            data={'chat_id': user.telegram_chat_id, 'text': message}
        )