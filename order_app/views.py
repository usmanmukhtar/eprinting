from django.shortcuts import render
from core_app.mixins import APIResponseGenericViewMixin, CreateResponseMixin, SoftDeleteDestroyViewMixin, DeleteResponseMixin
from rest_framework.viewsets import ModelViewSet
from .models import (
    Order
)
from .serializers import (
    OrderSerializer
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from core_app.utils import specific_error_response, success_response, success_response_message
import math
from core_app.pagination import MetaPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.filters import SearchFilter
from  django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class OrderViewSet(APIResponseGenericViewMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields =['order_type']
    # http_method_names = ['POST', ]

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['user'] = request.user.pk
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_response_message(serializer.data, message="Created order successfully.")

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.queryset.filter(user_id=user.id))
        pagination = MetaPageNumberPagination()
        qs = pagination.paginate_queryset(queryset, request)
        serializer = OrderSerializer(qs, context={'request': request}, many=True)
        return pagination.get_paginated_response(serializer.data)