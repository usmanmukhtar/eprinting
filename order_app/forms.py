from django.forms import ModelForm, ChoiceField
from .models import Order, OrderType

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    order_type = ChoiceField(
        choices=[
            (OrderType.ACCEPTED, "Accept"), 
            (OrderType.INPROGRESS, "In progress"),
            (OrderType.COMPLETED, "Complete"),
            (OrderType.CANCELED, "Cancel"),
        ]
    )