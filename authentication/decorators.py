from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .services.cognito_authentication import CognitoAuthentication
from .utils import get_user_id_from_token

User = get_user_model()


def cognito_authenticated(func):
    @wraps(func)
    def wrapper(view_instance, request, *args, **kwargs):
        try:
            user_id = get_user_id_from_token(request)
            try:
                user = User.objects.get(user_id=user_id)
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
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return wrapper
