from rest_framework import serializers

from .models import Budget, Operation, OperationCategory, Bank


class BudgetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ("id", "amount", "categories", "banks",)
        
    amount = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    banks = serializers.SerializerMethodField()
    
    def get_amount(self, obj):
        return obj.amount
    
    def get_categories(self, obj):
        operation_category = OperationCategory.objects.filter(
            user=obj.user
        )
        data = OperationCategoryModelSerializer(operation_category, many=True).data
        return data
    
    def get_banks(self, obj):
        banks = Bank.objects.filter(
            user=obj.user
        )
        data = BankModelSerializer(banks, many=True).data
        return data
    
    
class OperationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ("id", "amount", "operation_type", "category", "bank", "description", "date_str",)

    date_str = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    bank = serializers.SerializerMethodField()
    
    def get_date_str(self, obj):
        date = obj.date if obj.date else obj.created_at
        return date.strftime("%d.%m.%Y %H:%M")
    
    def get_category(self, obj):
        return (
            OperationCategoryModelSerializer(obj.category).data
            if obj.category
            else None
        )
    
    def get_bank(self, obj):
        return (
            BankModelSerializer(obj.bank).data
            if obj.bank
            else None
        )
    
    
class BankModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("id", "title", "color",)
    
    
class OperationCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationCategory
        fields = ("id", "title", "color", "operation_type",)
