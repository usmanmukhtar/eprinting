import django_filters
from user_app.models import FavouritePlayers

class HomiesNameFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(field_name='favourite_player__full_name', lookup_expr='icontains')


    class Meta:
        model = FavouritePlayers
        fields = ['full_name']
