from rest_framework import serializers
from .models import Store, Service, Size, Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('__all__')

class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('__all__')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('__all__')


class ServiceSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    class Meta:
        model = Service
        fields = ('__all__')
