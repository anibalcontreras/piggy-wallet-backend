from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from .services.cognito_service import CognitoService
from django.conf import settings


cognito_service = CognitoService(
    region=settings.AWS_REGION,
    user_pool_id=settings.COGNITO_USER_POOL_ID,
    app_client_id=settings.COGNITO_APP_CLIENT_ID,
    app_client_secret=settings.COGNITO_APP_CLIENT_SECRET,
)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            phone = serializer.validated_data["phone"]
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                cognito_service.register_user(name, phone, email, password)
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                response = cognito_service.login_user(email, password)
                return Response(
                    {
                        "access_token": response["AuthenticationResult"]["AccessToken"],
                        "id_token": response["AuthenticationResult"]["IdToken"],
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
