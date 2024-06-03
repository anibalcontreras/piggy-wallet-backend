from django.http import JsonResponse
from authentication.decorators import cognito_authenticated


@cognito_authenticated
def hello_world(request):
    return JsonResponse({"message": "Hello, world!"})
