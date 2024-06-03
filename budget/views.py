# budget/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Budget
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_user_budget(request):
    user_id = request.user.get('sub')  # Assuming 'sub' is the user ID in Cognito token
    try:
        budget = Budget.objects.get(user_id=user_id)
        return JsonResponse({'user_id': user_id, 'budget': budget.amount})
    except Budget.DoesNotExist:
        return JsonResponse({'error': 'Budget not found'}, status=404)

@csrf_exempt
def set_user_budget(request):
    user_id = request.user.get('sub')
    amount = request.POST.get('amount')
    budget, created = Budget.objects.get_or_create(user_id=user_id, defaults={'amount': amount})
    if not created:
        budget.amount = amount
        budget.save()
    return JsonResponse({'user_id': user_id, 'budget': budget.amount})

@csrf_exempt
def delete_user_budget(request):
    user_id = request.user.get('sub')
    try:
        budget = Budget.objects.get(user_id=user_id)
        budget.delete()
        return JsonResponse({'message': 'Budget deleted'})
    except Budget.DoesNotExist:
        return JsonResponse({'error': 'Budget not found'}, status=404)
    
@csrf_exempt
def update_user_budget(request):
    user_id = request.user.get('sub')
    amount = request.POST.get('amount')
    try:
        budget = Budget.objects.get(user_id=user_id)
        budget.amount = amount
        budget.save()
        return JsonResponse({'user_id': user_id, 'budget': budget.amount})
    except Budget.DoesNotExist:
        return JsonResponse({'error': 'Budget not found'}, status=404)