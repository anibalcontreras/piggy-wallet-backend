from rest_framework import viewsets, status
from rest_framework.response import Response
import jwt
from django.contrib.auth import get_user_model

from authentication.decorators import cognito_authenticated

from .models import Piggies
from .serializers import PiggiesSerializer


class PiggiesViewSet(viewsets.ViewSet):
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
            User = get_user_model()
            users = [{"user_id": str(x.user_id), "first_name": x.first_name} for x in User.objects.all()]

            filtered_users = []

            for user in users:
                if user["user_id"] != username:
                    filtered_users.append(user)

            piggies = Piggies.objects.filter(username=username)
            serializer = PiggiesSerializer(piggies, many=True)
            final_users = []

            for pig in serializer.data:
                for user in filtered_users:
                    if str(pig["piggy"]) == user["user_id"]:
                        final_users.append(user)

            return Response(data=final_users)
        except Piggies.DoesNotExist:
            return Response({"error": "Piggies not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            username = self.get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = username

            serializer = PiggiesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "username": serializer.data["username"],
                    "piggy": serializer.data["piggy"],
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotPiggiesViewSet(viewsets.ViewSet):
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

    def users(self, request):
        try:
            username = self.get_user_id_from_token(request)
            User = get_user_model()
            users = [{"user_id": str(x.user_id), "first_name": x.first_name, "email": x.email} for x in User.objects.all()]

            filtered_users = []

            for user in users:
                if user["user_id"] != username:
                    filtered_users.append(user)

            piggies = Piggies.objects.filter(username=username)
            serializer = PiggiesSerializer(piggies, many=True)

            if len(serializer.data) == 0:
                return Response(data=filtered_users)

            final_users = []

            for pig in serializer.data:
                for user in filtered_users:
                    if str(pig["piggy"]) != user["user_id"]:
                        final_users.append(user)

            return Response(data=final_users)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
