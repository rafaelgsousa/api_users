from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import CustomUser


@receiver(post_save, sender=RefreshToken)
def token_expired(sender, instance, **kwargs):
    if instance.blacklisted_at:
        user = CustomUser.objects.get(id=instance.user.id)

        user.is_logged_in = False
        user.save()