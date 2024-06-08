from django.db import models
from users.models import User

from common.models import SimpleBaseModel


class OperationCategory(SimpleBaseModel):
    class Meta:
        ordering = ("-created_at",)

    REPLENISHMENT = "REPLENISHMENT"
    FORGIVENESS = "FORGIVENESS"

    OPERATION_TYPE = (
        (REPLENISHMENT, REPLENISHMENT),
        (FORGIVENESS, FORGIVENESS),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=50, choices=OPERATION_TYPE)
    title = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
