from rest_framework import viewsets, status
from rest_framework.response import Response
import jwt
from django.contrib.auth import get_user_model

from authentication.decorators import cognito_authenticated
from authentication.utils import get_user_id_from_token

from .models import Piggies
from .serializers import PiggiesSerializer


class PiggiesViewSet(viewsets.ViewSet):
    @cognito_authenticated
    def list(self, request):
        try:
            username = get_user_id_from_token(request)
            User = get_user_model()
            users = [{"user_id": str(x.user_id), "first_name": x.first_name} for x in User.objects.all()]

            filtered_users = []

            for user in users:
                if user["user_id"] != username:
                    filtered_users.append(user)

            piggies = Piggies.objects.filter(username=username)
            serializer = PiggiesSerializer(piggies, many=True)
            final_users = []
            piggies_id = [str(pig["piggy"]) for pig in serializer.data]

            for user in filtered_users:
                if user["user_id"] in piggies_id:
                    final_users.append(user)

            return Response(data=final_users)
        except Piggies.DoesNotExist:
            return Response({"error": "Piggies not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            username = get_user_id_from_token(request)
            data = request.data.copy()
            data["username"] = username

            serializer = PiggiesSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                response = {
                    "username": serializer.data["username"],
                    "piggy": serializer.data["piggy"],
                }

                serializer = PiggiesSerializer(data={"username": data["piggy"], "piggy": username})

                if serializer.is_valid():
                    serializer.save()

                    return Response(data=response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotPiggiesViewSet(viewsets.ViewSet):
    def users(self, request):
        try:
            username = get_user_id_from_token(request)
            User = get_user_model()
            users = [
                {"user_id": str(x.user_id), "first_name": x.first_name, "email": x.email} for x in User.objects.all()
            ]

            filtered_users = []

            for user in users:
                if user["user_id"] != username:
                    filtered_users.append(user)

            piggies = Piggies.objects.filter(username=username)
            serializer = PiggiesSerializer(piggies, many=True)

            if len(serializer.data) == 0:
                return Response(data=filtered_users)

            final_users = []
            piggies_id = [str(pig["piggy"]) for pig in serializer.data]

            for user in filtered_users:
                if user["user_id"] not in piggies_id:
                    final_users.append(user)

            return Response(data=final_users)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
