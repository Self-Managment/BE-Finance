from django.db import models
from users.models import User

from common.models import SimpleBaseModel


class Bank(SimpleBaseModel):
    class Meta:
        ordering = ("created_at",)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
