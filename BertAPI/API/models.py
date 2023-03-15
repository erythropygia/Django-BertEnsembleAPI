from django.db import models

#API usage control libraries
import datetime
from django.contrib.auth.models import User

#API usage control model
class UserUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
