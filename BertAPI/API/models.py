from django.db import models

import datetime
from django.contrib.auth.models import User

class UserUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
