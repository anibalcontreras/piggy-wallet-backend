from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer
from .services.cognito_service import CognitoService
from django.conf import settings
from .models import User
from .decorators import cognito_authenticated
import jwt


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
                        "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh_token"]
            user_sub = serializer.validated_data["user_sub"]
            try:
                response = cognito_service.refresh_tokens(refresh_token, user_sub)
                return Response(
                    {
                        "access_token": response["AuthenticationResult"]["AccessToken"],
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get_user_id_from_token(self, request):
        try:
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                raise Exception("Authorization header not found")

            token = authorization_header.split()[1]
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded_token.get("username")
            if not user_id:
                raise Exception("User ID not found in token")
            return user_id
        except jwt.DecodeError:
            raise Exception("Invalid token")
        except jwt.ExpiredSignatureError:
            raise Exception("Expired token")
        except Exception as e:
            raise Exception(f"Error decoding token: {e}")

    @cognito_authenticated
    def get(self, request):
        try:
            username = self.get_user_id_from_token(request)
            user = User.objects.get(user_id=username)
            return Response(
                {"user_id": user.user_id, "first_name": user.first_name, "email": user.email},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
