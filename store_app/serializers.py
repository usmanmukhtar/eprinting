from rest_framework import serializers
from .models import Store, Service, Size, StoreRating
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Avg
from user_app.serializers import UserProfileSerializer
from user_app.models import UserProfile

class StoreSerializer(serializers.ModelSerializer):
    store_image = serializers.ImageField(source='user.image')
    start_time = serializers.SerializerMethodField(read_only=True)
    end_time = serializers.SerializerMethodField(read_only=True)
    is_online = serializers.SerializerMethodField(read_only=True)
    total_ratings = serializers.SerializerMethodField(read_only=True)

    def get_start_time(self, store):
        return store.start_time.time()

    def get_end_time(self, store):
        return store.end_time.time()

    def get_is_online(self, store):
        now = timezone.now().time()
        start_time = store.start_time.time()
        end_time = store.end_time.time()

        # Check if the store is online for 24 hours
        if start_time == end_time:
            return True

        # If the end time is less than the start time, it means the store is open overnight.
        if end_time < start_time:
            # The store is online if current time is after start time or before end time.
            return now >= start_time or now <= end_time
        else:
            # Standard check for cases where the store's end time is after its start time.
            return start_time <= now <= end_time

    def get_total_ratings(self, store):
        ratings = StoreRating.objects.filter(store_id=store.id).aggregate(ratings=Coalesce(Avg('rate'), 0, output_field=DecimalField()))
        return ratings.get('ratings')

    class Meta:
        model = Store
        fields = ('__all__')

class StoreDetailSerializer(serializers.ModelSerializer):
    store_image = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField(read_only=True)
    end_time = serializers.SerializerMethodField(read_only=True)
    is_online = serializers.SerializerMethodField(read_only=True)
    services = serializers.SerializerMethodField(read_only=True)
    total_ratings = serializers.SerializerMethodField(read_only=True)

    def get_store_image(self, store):
        request = self.context.get('request')
        image_path = store.user.image.url if store.user.image else None
        if image_path and request is not None:
            return request.build_absolute_uri(image_path)
        return image_path

    def get_start_time(self, store):
        return store.start_time.time()

    def get_end_time(self, store):
        return store.end_time.time()

    def get_is_online(self, store):
        now = timezone.now().time()
        start_time = store.start_time.time()
        end_time = store.end_time.time()

        # Check if the store is online for 24 hours
        if start_time == end_time:
            return True

        # If the end time is less than the start time, it means the store is open overnight.
        if end_time < start_time:
            # The store is online if current time is after start time or before end time.
            return now >= start_time or now <= end_time
        else:
            # Standard check for cases where the store's end time is after its start time.
            return start_time <= now <= end_time

    def get_services(self, store):
        request = self.context.get('request')
        services = Service.objects.filter(store=store)[:6]

        return ServiceSerializer(services, context={'request': request}, many=True).data

    def get_total_ratings(self, store):
        ratings = StoreRating.objects.filter(store_id=store.id).aggregate(ratings=Coalesce(Avg('rate'), 0, output_field=DecimalField()))
        return ratings.get('ratings')

    class Meta:
        model = Store
        fields = ('__all__')

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('__all__')

class ServiceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, service):
        request = self.context.get('request')
        image_path = service.image.url if service.image else None
        if image_path and request is not None:
            return request.build_absolute_uri(image_path)
        return image_path
    sizes = SizeSerializer(many=True)

    class Meta:
        model = Service
        fields = ('__all__')

class StoreRatingSerializer(serializers.ModelSerializer):
    liked_by_detail = serializers.SerializerMethodField()
    class Meta:
        model = StoreRating
        fields = ('__all__')
    
    def get_liked_by_detail(self, obj):
        # Serialize the UserProfile instance associated with 'liked_by'
        serializer = UserProfileSerializer(obj.liked_by)
        return serializer.data