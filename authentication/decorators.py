from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from .services.cognito_authentication import CognitoAuthentication


def cognito_authenticated(func):
    @wraps(func)
    @api_view(["GET", "POST", "PUT", "DELETE"])
    @authentication_classes([CognitoAuthentication])
    def wrapper(request, *args, **kwargs):
        if not request.user or not hasattr(request.user, "get"):
            return Response(
                {"error": "Authentication credentials were not provided or are invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return func(request, *args, **kwargs)

    return wrapper
