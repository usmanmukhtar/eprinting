from rest_framework import serializers
from .models import Store, Service, Size, StoreRating
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Avg

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
    store_image = serializers.ImageField(source='user.image')
    start_time = serializers.SerializerMethodField(read_only=True)
    end_time = serializers.SerializerMethodField(read_only=True)
    is_online = serializers.SerializerMethodField(read_only=True)
    services = serializers.SerializerMethodField(read_only=True)
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

    def get_services(self, store):
        services = Service.objects.filter(store=store)[:6]

        return ServiceSerializer(services, many=True).data

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
    sizes = SizeSerializer(many=True)
    class Meta:
        model = Service
        fields = ('__all__')

class StoreRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRating
        fields = ('__all__')