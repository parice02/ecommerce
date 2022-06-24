from django.shortcuts import render
from django.http import JsonResponse, Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import serializers, viewsets, permissions, decorators
from rest_framework import status


from .permissions import OrderReadWritePermission
from .serializers import OrderSerializer
from .models import Order

# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderReadWritePermission]

    @decorators.action(methods=["get"], detail=False)
    def user_orders(self, request, *args, **kwargs):
        user = request.GET.get("user", None)
        if not user:
            return Response(
                data={"details": "Problème de requête."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        orders = self.get_queryset().filter(client=user)
        serializer = self.get_serializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
