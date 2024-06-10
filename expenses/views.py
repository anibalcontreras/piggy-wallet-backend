from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense
from user_expense_type.models import UserExpenseType
from categories.models import Category
from .serializers import ExpenseSerializer
from authentication.decorators import cognito_authenticated
import jwt
from django.db.models import Sum
from django.utils.timezone import now


class ExpenseViewSet(viewsets.ViewSet):
    def get_user_id_from_token(self, request):
        try:
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                raise Exception("Authorization header not found")

            token = authorization_header.split()[1]
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            username = decoded_token.get("username")
            if not username:
                raise Exception("User ID not found in token")
            return username
        except jwt.DecodeError:
            raise Exception("Invalid token")
        except jwt.ExpiredSignatureError:
            raise Exception("Expired token")
        except Exception as e:
            raise Exception(f"Error decoding token: {e}")

    @cognito_authenticated
    def list(self, request):
        try:
            username = self.get_user_id_from_token(request)
            expenses = Expense.objects.filter(username=username)
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data)
        except Expense.DoesNotExist:
            return Response({"error": "Expenses not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            username = self.get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = username

            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def destroy(self, request):
        try:
            username = self.get_user_id_from_token(request)
            id = request.data.get("id")
            expense = Expense.objects.get(id=id, username=username)
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def partial_update(self, request):
        try:
            username = self.get_user_id_from_token(request)
            id = request.data.get("id")
            expense = Expense.objects.get(id=id, username=username)
            serializer = ExpenseSerializer(expense, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseGroupedByTypeAndCategoryViewSet(viewsets.ViewSet):
    def get_user_id_from_token(self, request):
        try:
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                raise Exception("Authorization header not found")

            token = authorization_header.split()[1]
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            username = decoded_token.get("username")
            if not username:
                raise Exception("User ID not found in token")
            return username
        except jwt.DecodeError:
            raise Exception("Invalid token")
        except jwt.ExpiredSignatureError:
            raise Exception("Expired token")
        except Exception as e:
            raise Exception(f"Error decoding token: {e}")

    @cognito_authenticated
    def list(self, request):
        try:
            username = self.get_user_id_from_token(request)
            expenses_grouped = {}
            today = now()
            expenses = (
                Expense.objects.filter(username=username, created_at__year=today.year, created_at__month=today.month)
                .values("expense_type_id", "category_id")
                .annotate(total_amount=Sum("amount"))
            )

            for expense in expenses:
                expense_type_name = UserExpenseType.objects.get(id=expense["expense_type_id"]).name
                category_name = Category.objects.get(id=expense["category_id"]).name
                total_amount = expense["total_amount"]

                if expense_type_name not in expenses_grouped:
                    expenses_grouped[expense_type_name] = {}

                expenses_grouped[expense_type_name][category_name] = total_amount

            return Response(expenses_grouped)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
