from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response
from authentication.decorators import cognito_authenticated


class CategoryViewSet(viewsets.ModelViewSet):
    @cognito_authenticated
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @cognito_authenticated
    def retrieve(self, request, pk=None):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
