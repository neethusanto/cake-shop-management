from django import forms
from .models import Booking
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['delivery_date', 'delivery_time', 'quantity', 'flavor_preference',
                  'custom_message', 'special_instructions', 'delivery_address']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': str(timezone.now().date())}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 50}),
            'flavor_preference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Chocolate, Vanilla'}),
            'custom_message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message on cake (optional)'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter delivery address'})
    )
    delivery_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Special instructions (optional)'})
    )
