from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import viewsets, status, decorators


from .permissions import ProductReadWritePermission
from .serializers import ProductSerializer
from .models import Product, History

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductReadWritePermission]

    @decorators.action(methods=["get"], detail=False, url_name="name")
    def find_by_name(self, request, *args, **kwargs):
        name = request.GET.get("q", None)
        print(name)
        if not name:
            return Response(
                data={"details": "Problème de requête."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(self.get_queryset(), designation=name)
        serializer = self.get_serializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @decorators.action(methods=["get"], detail=False, url_name="search")
    def search(self, request, *args, **kwargs):
        q = request.GET.get("q", None)
        if not q:
            return Response(
                data={"details": "Problème de requête."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        products = self.get_queryset().filter(
            Q(designation__icontains=q) | Q(description__icontains=q)
        )
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @decorators.action(methods=["get"], detail=True, url_name="buy")
    def buy(self, request, *args, **kwargs):
        quantity = request.GET.get("qty", None)
        if not quantity:
            return Response(
                data={"details": "Problème de requête."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            quantity = float(quantity)
        except Exception as exp:
            return Response(
                data={"details": "Problème de requête.", "info": exp.__str__()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = self.get_object()
        if product.stock - quantity < 0:
            return Response(
                data={
                    "details": "La quantité restante n'est pas suffisante pour cette opération."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product.stock -= quantity
        product.save()
        History.objects.create(
            product=product, quantity=quantity, transaction="purchase"
        )

        return Response(data={"details": "success"}, status=status.HTTP_200_OK)

    @decorators.action(methods=["get"], detail=True, url_name="supply")
    def add_stock(self, request, *args, **kwargs):
        quantity = request.GET.get("qty", None)
        if not quantity:
            return Response(
                data={"details": "Problème de requête."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            quantity = float(quantity)
        except Exception as exp:
            return Response(
                data={"details": "Problème de requête.", "info": exp.__str__()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = self.get_object()
        product.stock += quantity
        product.save()
        History.objects.create(
            product=product, quantity=quantity, transaction="storage"
        )

        return Response(data={"details": "success"}, status=status.HTTP_200_OK)
