from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Ensure every new account has a role profile."""
    if not created:
        return
    if instance.is_superuser:
        default_role = "admin"
    elif instance.is_staff:
        default_role = "teacher"
    else:
        default_role = "student"
    UserProfile.objects.get_or_create(user=instance, defaults={"role": default_role})
