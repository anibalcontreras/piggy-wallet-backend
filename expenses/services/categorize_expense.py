from rest_framework.response import Response
from rest_framework import status
from categories.models import Category
from AI.AI import get_category_name_from_description
from categories.exceptions import InvalidCategoryError


def categorize_expense_description(data):
    if "description" in data:
        try:
            category_name = get_category_name_from_description(data["description"])
            category_obj = Category.objects.get(name=category_name)
            data["category"] = category_obj.id
            return data, None
        except ValueError as e:
            return None, Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidCategoryError as e:
            return None, Response({"error": str(e)}, status=e.code)
    else:
        return None, Response({"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)
