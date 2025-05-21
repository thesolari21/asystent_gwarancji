from django import forms
from .models import Receipt
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ('name', 'description', 'date_purchase', 'lenght_of_warranty','image','attachment')
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'date_purchase': 'Data zakupu',
            'lenght_of_warranty': 'Długość gwarancji (msc)',
            'image': 'Załącznik screen',
            'attachment': 'Załącznik PDF',

        }

        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise ValidationError("Tylko pliki PDF są dozwolone.")
            if file.content_type != 'application/pdf':
                raise ValidationError("Załącznik musi być plikiem PDF.")
        return file


class CustomAuthenticationForm(AuthenticationForm):
    # Możesz dostosować ten formularz, dodając własne pola lub zmieniając ich etykiety itp.
    pass