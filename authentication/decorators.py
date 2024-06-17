from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .services.cognito_authentication import CognitoAuthentication

User = get_user_model()


def cognito_authenticated(func):
    @wraps(func)
    def wrapper(view_instance, request, *args, **kwargs):
        auth = CognitoAuthentication()
        try:
            result = auth.authenticate(request)
            if result is None:
                return Response(
                    {"error": "Authentication credentials were not provided or are invalid."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            user_payload, auth_error = result
            if auth_error or not user_payload:
                return Response(
                    {"error": "Authentication credentials were not provided or are invalid."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            try:
                user = User.objects.get(user_id=user_payload["sub"])
                request.user = user
            except User.DoesNotExist:
                return Response(
                    {"error": "Authenticated user not found."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return func(view_instance, request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Authentication failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
