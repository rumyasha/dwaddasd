from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    email = models.EmailField(unique=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    receive_email_notifications = models.BooleanField(default=True)
    receive_telegram_notifications = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    favorite_recipes = models.ManyToManyField('recipes.Recipe', related_name='favorited_by', blank=True)
    saved_recipes = models.ManyToManyField('recipes.Recipe', related_name='saved_by', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()