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
from authentication.utils import get_user_id_from_token
from expenses.services.categorize_expense import categorize_expense_description


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
            username = get_user_id_from_token(request)
            expenses = Expense.objects.filter(username=username)

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            if start_date and end_date:
                expenses = expenses.filter(created_at__range=[start_date, end_date])
            elif start_date:
                expenses = expenses.filter(created_at__gte=start_date)
            elif end_date:
                expenses = expenses.filter(created_at__lte=end_date)
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data)
        except Expense.DoesNotExist:
            return Response({"error": "Expenses not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def retrieve(self, request, pk=None):
        try:
            username = get_user_id_from_token(request)
            expense = Expense.objects.get(id=pk, username=username)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            username = get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = username

            data, error_response = categorize_expense_description(data)
            if error_response:
                return error_response

            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def destroy(self, request, pk=None):
        try:
            username = get_user_id_from_token(request)
            expense = Expense.objects.get(id=pk, username=username)
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def partial_update(self, request, pk=None):
        try:
            username = get_user_id_from_token(request)
            expense = Expense.objects.get(id=pk, username=username)
            serializer = ExpenseSerializer(expense, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseGroupedByTypeAndCategoryViewSet(viewsets.ViewSet):
    @cognito_authenticated
    def list(self, request):
        try:
            username = get_user_id_from_token(request)
            expenses_grouped = {}
            today = now()
            expenses = (
                Expense.objects.filter(username=username, created_at__year=today.year, created_at__month=today.month)
                .values("user_expense_type_id", "category_id")
                .annotate(total_amount=Sum("amount"))
            )

            for expense in expenses:
                user_expense_type = UserExpenseType.objects.get(id=expense["user_expense_type_id"])
                category = Category.objects.get(id=expense["category_id"])
                total_amount = expense["total_amount"]

                if user_expense_type.name not in expenses_grouped:
                    expenses_grouped[user_expense_type.name] = {}

                expenses_grouped[user_expense_type.name][category.name] = total_amount

            return Response(expenses_grouped)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
