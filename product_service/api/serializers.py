from rest_framework import serializers

from .models import Product, History


class ProductSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = Product
        fields = "__all__"


class HistorySerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = History
        fields = "__all__"
