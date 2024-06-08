from .models import Operation, OperationCategory
from users.models import User
from .serializers import OperationModelSerializer


def get_operation_statistic(user):    
    data = {}
    
    categories = OperationCategory.objects.filter(user=user)
    
    for operation_type in Operation.OPERATION_TYPE_LIST:
        operation_data = {
            "values": [],
            "labels": [],
            "colors": [],
        }
        
        for category in categories:
            operation_sum = sum(
                Operation.objects.filter(
                    operation_type=operation_type,
                    budget__user=user,
                    category=category,
                )
                .values_list("amount", flat=True)
            )
            if operation_sum:
                label = category.title
                color = category.color
                
                operation_data["values"].append(operation_sum)
                operation_data["labels"].append(label)
                operation_data["colors"].append(color)
            
        other_operation_sum = sum(
            Operation.objects.filter(
                operation_type=Operation.REPLENISHMENT,
                budget__user=user,
                category__isnull=True,
            )
            .values_list("amount", flat=True)
        )
        if other_operation_sum:
            operation_data["labels"].append("Другое")
            operation_data["colors"].append("#969696")
            operation_data["values"].append(other_operation_sum)
            
        data[operation_type] = operation_data
    
    return data


def get_operation_history(operations: list[Operation]) -> dict:
    dates = {}
    for operation in operations:
        date = operation.date.strftime("%d.%m.%Y")
        operation = OperationModelSerializer(operation).data
        dates[date] = dates.get(date, []) + [operation]
        
    return dates
    