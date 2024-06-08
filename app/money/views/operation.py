from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from money.serializers import OperationCategoryModelSerializer, OperationModelSerializer
from money.models import Budget, Operation, OperationCategory

from money.utils import get_operation_statistic, get_operation_history

from django.db.models import Q

import datetime


class OperationHistoryView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        filters = request.GET
        operation_type = filters.get("operation_type")
        category_id = filters.get("category_id")
        bank_id = filters.get("bank_id")
        order_by = filters.get("order_by")
        
        filters = Q()
        
        if operation_type:
            filters &= Q(operation_type=operation_type)
        if category_id:
            filters &= Q(category_id=category_id)
        if bank_id:
            filters &= Q(bank_id=bank_id)
        
        operations = (
            Operation.objects
            .filter(budget__user=request.user)
            .filter(filters)
            .order_by(
                "date"
                if order_by == "asc"
                else "-date"
            )
        )
        
        data = get_operation_history(operations)
        return Response(data, status=status.HTTP_200_OK)
    
    
class OperationView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        filters = request.GET
        operation_type = filters.get("operation_type")
        category_id = filters.get("category_id")
        bank_id = filters.get("bank_id")
        order_by = filters.get("order_by")
        
        filters = Q()
        
        if operation_type:
            filters &= Q(operation_type=operation_type)
        if category_id:
            filters &= Q(category_id=category_id)
        if bank_id:
            filters &= Q(bank_id=bank_id)
        
        operations = (
            Operation.objects
            .filter(budget__user=request.user)
            .filter(filters)
            .order_by(
                "date"
                if order_by == "asc"
                else "-date"
            )
        )
        
        data = OperationModelSerializer(
            operations,
            many=True,
        ).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        operation_type = data.get("operation_type")
        
        if operation_type not in Operation.OPERATION_TYPE_LIST:
            return Response(
                {"error": "Передан неверный тип операции"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        budget, _ = Budget.objects.get_or_create(user=user)
        date_str: str | None = data.get("date")
        date = (
            datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
            if date_str
            else datetime.datetime.now()
        )
        
        Operation(
            budget=budget,
            amount=data.get("amount"),
            operation_type=operation_type,
            category_id=data.get("category"),
            bank_id=data.get("bank"),
            description=data.get("description"),
            date=date,
        ).save()
        return Response({}, status=status.HTTP_201_CREATED)
    
    
class OperationStatisticView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        data = get_operation_statistic(request.user)
        
        return Response(data, status=status.HTTP_200_OK)
    
    
class OperationCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = OperationCategoryModelSerializer
        
        operation_category = OperationCategory.objects.filter(
            user=user
        )
        
        data = serializer(operation_category, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        title = data.get("title")
        color = data.get("color")
        operation_type = data.get("operation_type")
        
        operation_category_exist = (
            OperationCategory.objects
            .filter(
                user=user,
                title__iexact=title.lower()
            )
            .last()
        )
        
        if operation_category_exist and operation_category_exist.operation_type == operation_type:
            operation_category_exist.title = title
            operation_category_exist.color = color
            operation_category_exist.save()
        else:
            OperationCategory(
                user=user,
                title=title,
                color=color,
                operation_type=operation_type,
            ).save()
        return Response({}, status=status.HTTP_201_CREATED)