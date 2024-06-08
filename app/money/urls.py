from django.urls import path

from .views import (
    BudgetView,
    OperationView,
    OperationHistoryView,
    OperationCategoryView,
    OperationStatisticView,
    BankView,
)

urlpatterns = [
    path("budget/", BudgetView.as_view(), name="budget"),
    path("operation/", OperationView.as_view(), name="operation"),
    path("operation/history", OperationHistoryView.as_view(), name="operation_history"),
    path("operation/category", OperationCategoryView.as_view(), name="operation_category"),
    path("operation/statistic", OperationStatisticView.as_view(), name="operation_statistic"),
    path("bank/", BankView.as_view(), name="bank")
]
