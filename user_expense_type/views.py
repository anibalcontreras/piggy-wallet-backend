from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserExpenseType
from .serializers import UserExpenseTypeSerializer
from authentication.decorators import cognito_authenticated
from authentication.utils import get_user_id_from_token
import jwt


class UserExpenseTypeViewSet(viewsets.ViewSet):
    @cognito_authenticated
    def list(self, request):
        try:
            username = get_user_id_from_token(request)
            user_expense_types = UserExpenseType.objects.filter(username=username)
            serializer = UserExpenseTypeSerializer(user_expense_types, many=True)
            return Response(data=serializer.data)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def retrieve(self, request, pk=None):
        try:
            username = get_user_id_from_token(request)
            user_expense_type = UserExpenseType.objects.get(id=pk, username=username)
            serializer = UserExpenseTypeSerializer(user_expense_type)
            return Response(data=serializer.data)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            username = get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = username

            serializer = UserExpenseTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def destroy(self, request, pk=None):
        try:
            username = get_user_id_from_token(request)
            user_expense_type = UserExpenseType.objects.get(id=pk, username=username)
            user_expense_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def partial_update(self, request, pk=None):
        try:
            username = get_user_id_from_token(request)
            user_expense_type = UserExpenseType.objects.get(id=pk, username=username)
            serializer = UserExpenseTypeSerializer(user_expense_type, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
