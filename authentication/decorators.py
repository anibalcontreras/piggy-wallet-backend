from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from .services.cognito_authentication import CognitoAuthentication


def cognito_authenticated(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        auth = CognitoAuthentication()
        try:
            result = auth.authenticate(request)
            if result is None:
                return Response(
                    {"error": "Authentication credentials were not provided or are invalid."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            user, auth_error = result
            if auth_error or not user:
                return Response(
                    {"error": "Authentication credentials were not provided or are invalid."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            request.user = user
            return func(self, request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Authentication failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
