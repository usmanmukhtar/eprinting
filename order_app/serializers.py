from rest_framework import serializers
from .models import Order
from rest_framework.fields import CharField
from store_app.serializers import StoreSerializer

class OrderSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    # pickup_time = serializers.SerializerMethodField()
    # orientation_display = CharField(source="get_orientation_display")
    order_type_display = CharField(source="get_order_type_display", read_only=True)
    store_detail = StoreSerializer(source="store", read_only=True)

    def get_total_price(self, order):
        return order.service.price + order.size.price
    
    # def get_pickup_time(self, order):
    #     return order.pickup_time.time()

    def get_document(self, order):
        request = self.context.get('request')
        document_path = order.document.url if order.document else None
        if document_path and request is not None:
            return request.build_absolute_uri(document_path)
        return document_path
    class Meta:
        model = Order
        fields = ('__all__')