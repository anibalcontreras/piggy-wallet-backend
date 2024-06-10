# budget/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Budget
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def get_user_budget(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required in the query parameters.'}, status=400)

            budget = Budget.objects.get(user_id=user_id)
            return JsonResponse({'user_id': int(user_id), 'amount': budget.amount})
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def set_user_budget(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            amount = data.get('amount')

            if not user_id or not amount:
                return JsonResponse({'error': 'User ID and amount are required.'}, status=400)

            budget = Budget.objects.create(user_id=user_id, amount=amount)
            budget.save()

            return JsonResponse({'message': 'Budget created successfully.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def delete_user_budget(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            budget = Budget.objects.get(user_id=user_id)
            budget.delete()

            return JsonResponse({'message': 'Budget deleted successfully', 'user_id': user_id})
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def update_user_budget(request):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            amount = data.get('amount')

            budget = Budget.objects.get(user_id=user_id)
            budget.amount = amount
            budget.save()

            return JsonResponse({'user_id': user_id, 'budget': budget.amount})
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
