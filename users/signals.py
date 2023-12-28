from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(post_save, sender=RefreshToken)
def token_expired(sender, instance, **kwargs):
    if instance.blacklisted_at:
        # O token expirou, você pode acessar os detalhes do usuário associado ao token
        user = User.objects.get(id=instance.user.id)

        # Atualize o campo desejado no modelo do usuário
        user.is_logged_in = False
        user.save()