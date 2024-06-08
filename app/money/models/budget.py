from django.db import models
from users.models import User

from common.models import SimpleBaseModel

from .operation import Operation


class Budget(SimpleBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def amount(self):
        summ = 0

        replenishments = Operation.objects.filter(
            budget=self,
            operation_type=Operation.REPLENISHMENT,
        ).all()
        summ += sum(_.amount for _ in replenishments)

        forgiveness = Operation.objects.filter(
            budget=self,
            operation_type=Operation.FORGIVENESS,
        ).all()
        summ -= sum(_.amount for _ in forgiveness)

        return summ
