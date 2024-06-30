from rest_framework import viewsets, status
from rest_framework.response import Response

from authentication.decorators import cognito_authenticated
from authentication.utils import get_user_id_from_token

from .models import BankCard
from .serializers import BankCardSerializer


class BankCardViewSet(viewsets.ViewSet):
    @cognito_authenticated
    def list(self, request):
        try:
            user_id = get_user_id_from_token(request)
            cards = BankCard.objects.filter(user_id=user_id)
            serializer = BankCardSerializer(cards, many=True)

            if len(serializer.data) == 0:
                default = BankCardSerializer(data={"user_id": user_id, "account_number": 0, "bank_name": "None", "card_type": "default"})

                if default.is_valid():
                    default.save()

                    return Response([default.data])

            return Response(serializer.data)
        except BankCard.DoesNotExist:
            return Response({"error": "Bank cards not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def create(self, request):
        try:
            user_id = get_user_id_from_token(request)
            data = request.data.copy()
            data["user_id"] = user_id

            serializer = BankCardSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def retrieve(self, request, pk=None):
        try:
            user_id = get_user_id_from_token(request)
            card = BankCard.objects.get(id=pk, user_id=user_id)
            serializer = BankCardSerializer(card)
            return Response(data=serializer.data)
        except BankCard.DoesNotExist:
            if pk == 1:
                default = BankCardSerializer(data={"user_id": user_id, "account_number": 0, "bank_name": "None", "card_type": "default"})

                if default.is_valid():
                    default.save()

                    return Response(default.data)

            return Response({"error": "Bank card not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def destroy(self, request, pk=None):
        try:
            user_id = get_user_id_from_token(request)
            card = BankCard.objects.get(id=pk, user_id=user_id)
            card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BankCard.DoesNotExist:
            return Response({"error": "Bank card not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cognito_authenticated
    def partial_update(self, request, pk=None):
        try:
            user_id = get_user_id_from_token(request)
            card = BankCard.objects.get(id=pk, user_id=user_id)
            serializer = BankCardSerializer(card, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BankCard.DoesNotExist:
            return Response({"error": "Bank card not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
