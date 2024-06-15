from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserExpenseType
from .serializers import UserExpenseTypeSerializer
from authentication.decorators import cognito_authenticated
import jwt


class UserExpenseTypeViewSet(viewsets.ViewSet):
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
            user_expense_types = UserExpenseType.objects.filter(username=username)
            serializer = UserExpenseTypeSerializer(user_expense_types, many=True)
            for ser in serializer.data:
                ser.pop("username")
                ser.pop("created_at")
                ser.pop("updated_at")
            return Response(data=serializer.data)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def retrieve(self, request, pk=None):
        try:
            username = self.get_user_id_from_token(request)
            user_expense_type = UserExpenseType.objects.get(id=pk, username=username)
            serializer = UserExpenseTypeSerializer(user_expense_type)
            response = {
                "name": serializer.data["name"],
                "description": serializer.data["description"],
                "set_by_user": serializer.data["set_by_user"],
            }
            return Response(data=response)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            username = self.get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = username

            serializer = UserExpenseTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "name": serializer.data["name"],
                    "description": serializer.data["description"],
                    "set_by_user": serializer.data["set_by_user"],
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def destroy(self, request, pk=None):
        try:
            username = self.get_user_id_from_token(request)
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
            username = self.get_user_id_from_token(request)
            user_expense_type = UserExpenseType.objects.get(id=pk, username=username)
            serializer = UserExpenseTypeSerializer(user_expense_type, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "name": serializer.data["name"],
                    "description": serializer.data["description"],
                    "set_by_user": serializer.data["set_by_user"],
                }
                return Response(data=response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserExpenseType.DoesNotExist:
            return Response({"error": "UserExpenseType not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
