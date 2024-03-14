from django import forms
from .models import Receipt
from django.contrib.auth.forms import AuthenticationForm

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ('name', 'description', 'date_purchase', 'lenght_of_warranty','image')
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'date_purchase': 'Data zakupu',
            'lenght_of_warranty': 'Długość gwarancji (msc)',
            'image': 'Załącznik',

        }

        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    # Możesz dostosować ten formularz, dodając własne pola lub zmieniając ich etykiety itp.
    pass