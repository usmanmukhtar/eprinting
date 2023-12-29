from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile
from store_app.models import Store

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('mobile_number', 'gender')  # Add any other fields if necessary

class StoreForm(forms.ModelForm):
    name = forms.CharField(
        label='Store Name',
        max_length=500,
        required=True,
    )
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    address = forms.CharField(
        label='Address (Format: Address, City, State, Zipcode)',
        max_length=500,
        required=True,
        help_text='Please enter in the format: Address, City, State, Zipcode'
    )
    latitude = forms.CharField(
        label='Latitude',
        max_length=500,
        required=True
    )
    longitude = forms.CharField(
        label='Longitude',
        max_length=500,
        required=True
    )


    class Meta:
        model = Store
        fields = ('name', 'address', 'latitude', 'longitude', 'start_time', 'end_time')
