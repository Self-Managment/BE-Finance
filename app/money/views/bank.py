from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from money.serializers import BankModelSerializer
from money.models import Bank
    
    
class BankView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = BankModelSerializer
        
        banks = Bank.objects.filter(
            user=user
        )
        
        data = serializer(banks, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        title = data.get("title")
        color = data.get("color")
        
        bank_exist = (
            Bank.objects
            .filter(
                user=user,
                title__iexact=title.lower()
            )
            .last()
        )
        
        if bank_exist:
            bank_exist.title = title
            bank_exist.color = color
            bank_exist.save()
        else:
            Bank(
                user=user,
                title=data.get("title"),
                color=data.get("color"),
            ).save()
        return Response({}, status=status.HTTP_201_CREATED)