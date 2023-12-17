from django.shortcuts import render
from core_app.mixins import APIResponseGenericViewMixin, CreateResponseMixin, SoftDeleteDestroyViewMixin, DeleteResponseMixin
from rest_framework.viewsets import ModelViewSet
from .models import (
    Store,
    Service,
)
from .serializers import (
    StoreSerializer,
    ServiceSerializer
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
from rest_framework.permissions import IsAuthenticated


class ServiceViewSet(APIResponseGenericViewMixin, ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Service, pk=pk)
        serializer = self.get_serializer(obj)

        return success_response_message(serializer.data, message="Retrieved data successfully.")



class StoreViewSet(APIResponseGenericViewMixin, ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # Earth radius in kilometers

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (math.sin(d_lat / 2) ** 2 +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(d_lon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    @action(detail=False, methods=['GET'])
    def nearby(self, request):
        # Get latitude and longitude from request
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        distance = request.query_params.get('distance', 5)  # Default distance is 5km

        if not latitude or not longitude:
            return specific_error_response("latitude and longitude are required")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            distance = float(distance)
        except ValueError:
            return specific_error_response("Invalid latitude, longitude or distance")

        # Calculate approximate bounding box for filtering
        # This uses a simple estimation and might not be perfectly accurate for large distances
        lat_range = distance / 111.32  # 1 degree of latitude ~ 111.32 km
        lon_range = distance / (111.32 * math.cos(latitude))

        # Filtering based on bounding box
        nearby_stores = Store.objects.filter(
            latitude__range=(latitude - lat_range, latitude + lat_range),
            longitude__range=(longitude - lon_range, longitude + lon_range)
        )

        data = []
        for store in nearby_stores:
            store_distance = self.haversine_distance(latitude, longitude, store.latitude, store.longitude)
            store_data = self.get_serializer(store).data
            store_data['distance'] = store_distance
            data.append(store_data)


        # serializer = self.get_serializer(queryset, many=True)
        return success_response_message(data, message="List Store Successfully")

    @action(detail=True, methods=['get'], url_path='services')
    def services(self, request, pk=None):
        queryset = Service.objects.filter(store=pk)
        paginator = MetaPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serialiser = ServiceSerializer(page, many=True)
        return paginator.get_paginated_response(serialiser.data)

