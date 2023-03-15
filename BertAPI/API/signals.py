#New member generate token signals
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#New member generate token signals
@receiver(post_migrate)
def create_auth_tokens(sender, **kwargs):
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)



