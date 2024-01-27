from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    def get_document(self, order):
        request = self.context.get('request')
        document_path = order.document.url if order.document else None
        if document_path and request is not None:
            return request.build_absolute_uri(document_path)
        return document_path
    class Meta:
        model = Order
        fields = ('__all__')