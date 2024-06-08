from django.db import models

from common.models import SimpleBaseModel


class Operation(SimpleBaseModel):
    class Meta:
        ordering = ("-date",)

    REPLENISHMENT = "REPLENISHMENT"
    FORGIVENESS = "FORGIVENESS"

    OPERATION_TYPE = (
        (REPLENISHMENT, REPLENISHMENT),
        (FORGIVENESS, FORGIVENESS),
    )

    OPERATION_TYPE_LIST = [
        REPLENISHMENT,
        FORGIVENESS,
    ]

    budget = models.ForeignKey("money.Budget", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    operation_type = models.CharField(max_length=50, choices=OPERATION_TYPE)
    category = models.ForeignKey(
        "money.OperationCategory", on_delete=models.SET_NULL, null=True
    )
    bank = models.ForeignKey("money.Bank", on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=25, null=True)
    date = models.DateTimeField(null=True)
