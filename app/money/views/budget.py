from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from money.serializers import BudgetModelSerializer
from money.models import Budget


class BudgetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = BudgetModelSerializer
        
        budget, _ = Budget.objects.get_or_create(user=user)
        
        data = serializer(budget).data
        return Response(data, status=status.HTTP_200_OK)