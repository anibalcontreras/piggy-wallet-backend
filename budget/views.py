from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Budget
from .serializers import BudgetSerializer
from authentication.decorators import cognito_authenticated
from authentication.utils import get_user_id_from_token


class BudgetViewSet(viewsets.ViewSet):
    @cognito_authenticated
    def list(self, request):
        try:
            user_id = get_user_id_from_token(request)
            budget = Budget.objects.filter(username=user_id).order_by("-created_at").first()
            if not budget:
                return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BudgetSerializer(budget)
            return Response(data={"amount": serializer.data["amount"]})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            user_id = get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = user_id

            serializer = BudgetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"amount": serializer.data["amount"]}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def destroy(self, request):
        try:
            user_id = get_user_id_from_token(request)
            budget = Budget.objects.filter(username=user_id).order_by("-created_at").first()
            if not budget:
                return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)
            budget.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def partial_update(self, request):
        try:
            user_id = get_user_id_from_token(request)
            budget = Budget.objects.filter(username=user_id).order_by("-created_at").first()
            if not budget:
                return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BudgetSerializer(budget, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"amount": serializer.data["amount"]})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
