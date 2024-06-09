from django.shortcuts import render
from django.http import JsonResponse
from .models import UserExpenseType
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def get_user_expense_types(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required in the query parameters.'}, status=400)
                
            user_expense_types = UserExpenseType.objects.filter(user_id=user_id)
            if not user_expense_types.exists():
                return JsonResponse({'error': 'User Expense Types not found'}, status=404)
            
            # Serializing the list of user expense types
            expense_types_list = [
                {
                    'id': expense_type.id,
                    'user_id': expense_type.user_id,
                    'name': expense_type.name,
                    'description': expense_type.description,
                    'set_by_user': expense_type.set_by_user,
                    'category_name': expense_type.category_name,
                    'created_at': expense_type.created_at,
                    'updated_at': expense_type.updated_at
                } for expense_type in user_expense_types
            ]
            
            return JsonResponse(expense_types_list, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def get_user_expense_type_by_name(request, name):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required in the query parameters.'}, status=400)
            
            user_expense_type = UserExpenseType.objects.get(user_id=user_id, name=name)
            return JsonResponse({
                'id': user_expense_type.id,
                'user_id': user_expense_type.user_id,
                'name': user_expense_type.name,
                'description': user_expense_type.description,
                'set_by_user': user_expense_type.set_by_user,
                'category_name': user_expense_type.category_name,
                'created_at': user_expense_type.created_at,
                'updated_at': user_expense_type.updated_at
            })
        except UserExpenseType.DoesNotExist:
            return JsonResponse({'error': 'User Expense Type not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def create_user_expense_type(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            name = data.get('name')
            description = data.get('description')
            set_by_user = data.get('set_by_user')
            category_name = data.get('category_name')
            
            if not user_id or not name or not category_name:
                return JsonResponse({'error': 'User ID, Name, and Category Name are required.'}, status=400)
            
            user_expense_type = UserExpenseType.objects.create(
                user_id=user_id, name=name, description=description, set_by_user=set_by_user, category_name=category_name
            )
            user_expense_type.save()
            
            return JsonResponse({'message': 'User Expense Type created successfully.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def update_user_expense_type(request, name):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            description = data.get('description')
            set_by_user = data.get('set_by_user')
            category_name = data.get('category_name')
            
            user_expense_type = UserExpenseType.objects.get(user_id=user_id, name=name)
            user_expense_type.description = description
            user_expense_type.set_by_user = set_by_user
            user_expense_type.category_name = category_name
            user_expense_type.save()
            
            return JsonResponse({'message': 'User Expense Type updated successfully.'})
        except UserExpenseType.DoesNotExist:
            return JsonResponse({'error': 'User Expense Type not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def delete_user_expense_type(request, name):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            user_expense_type = UserExpenseType.objects.get(user_id=user_id, name=name)
            user_expense_type.delete()
            
            return JsonResponse({'message': 'User Expense Type deleted successfully.'})
        except UserExpenseType.DoesNotExist:
            return JsonResponse({'error': 'User Expense Type not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
