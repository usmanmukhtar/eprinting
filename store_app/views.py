from django.shortcuts import render
from core_app.mixins import APIResponseGenericViewMixin, CreateResponseMixin, SoftDeleteDestroyViewMixin, DeleteResponseMixin
from rest_framework.viewsets import ModelViewSet
from .models import (
    Store,
    Service,
    FavoriteStore,
    StoreRating
)
from .serializers import (
    StoreSerializer,
    StoreDetailSerializer,
    ServiceSerializer,
    StoreRatingSerializer
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
from rest_framework.filters import SearchFilter

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
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, pk=None):
        store = get_object_or_404(Store, id=pk)
        serializer = StoreDetailSerializer(store).data
        return Response(serializer, status=status.HTTP_200_OK)

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
        is_favorite = bool(request.query_params.get('is_favorite', False))
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        distance = request.query_params.get('distance', 5)  # Default distance is 5km

        if is_favorite:
            favorite_stores = FavoriteStore.objects.filter(favorited_by=request.user.userprofile)
            stores = [favorite.store for favorite in favorite_stores]

            paginator = MetaPageNumberPagination()
            page = paginator.paginate_queryset(stores, request)

            if page is not None:
                # Serialize the page instead of the full queryset
                data = self.get_serializer(page, many=True).data
                return paginator.get_paginated_response(data)

            data = StoreSerializer(stores, many=True).data
            return success_response_message(data, message="List Store Successfully")

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
        nearby_stores = self.filter_queryset(self.get_queryset()).filter(
            latitude__range=(latitude - lat_range, latitude + lat_range),
            longitude__range=(longitude - lon_range, longitude + lon_range)
        )

        paginator = MetaPageNumberPagination()
        page = paginator.paginate_queryset(nearby_stores, request)

        data = []
        for store in page:
            store_distance = self.haversine_distance(latitude, longitude, store.latitude, store.longitude)
            store_data = self.get_serializer(store).data
            store_data['distance'] = store_distance
            data.append(store_data)

        if page is not None:
            # Serialize the page instead of the full queryset
            return paginator.get_paginated_response(data)

        data = StoreSerializer(nearby_stores, many=True).data
        return success_response_message(data, message="List Store Successfully")

    @action(detail=True, methods=['get'], url_path='services')
    def services(self, request, pk=None):
        queryset = Service.objects.filter(store=pk)
        paginator = MetaPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serialiser = ServiceSerializer(page, many=True)
        return paginator.get_paginated_response(serialiser.data)

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        queryset = StoreRating.objects.filter(store=pk)
        paginator = MetaPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serialiser = StoreRatingSerializer(page, many=True)
        return paginator.get_paginated_response(serialiser.data)

    @action(detail=True, methods=['post'], url_path='favorite')
    def favorite_store(self, request, pk=None):
        try:
            fav_obj = FavoriteStore.objects.get(store=pk, favorited_by=request.user.userprofile)
        except FavoriteStore.DoesNotExist as e:
            print(e)
            FavoriteStore.objects.create(favorited_by=request.user.userprofile, store_id=pk)
            return Response({"message": "Store Favorited"}, status=status.HTTP_200_OK)

        if fav_obj:
            fav_obj.delete()
            return Response({"message": "Store Unfavorited"}, status=status.HTTP_200_OK)

class ReviewViewSet(APIResponseGenericViewMixin, ModelViewSet):
    queryset = StoreRating.objects.all()
    serializer_class = StoreRatingSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request_data = request.data
        request_data['liked_by'] = request.user.userprofile.pk
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_response_message(serializer.data, message="Created rating successfully.")


    def update(self, request, pk, format=None):
        try:
            review = get_object_or_404(StoreRating, pk=pk)
            request_data = request.data
            request_data['liked_by'] = request.user.userprofile.pk
            serializer = self.get_serializer(review, data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer_data = serializer.data
            return success_response_message(serializer_data, message="Updated rating successfully.")
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
