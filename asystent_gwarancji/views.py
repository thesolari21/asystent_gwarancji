import datetime

from django.shortcuts import render, get_object_or_404
from asystent_gwarancji.models import Receipt
from django.http import HttpResponse
from .forms import ReceiptForm
from .forms import CustomAuthenticationForm
from django.shortcuts import redirect
from dateutil.relativedelta import relativedelta
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth import authenticate, login

# Create your views here.

def receipt(request):

    access = None
    for group in request.user.groups.all():
        if group.name == 'ag':
            access = True
        else:
            access = False

    receipts = Receipt.objects.filter(status=1)

    for r in receipts:
        delta = r.date_warranty_to - r.date_purchase
        r.delta = delta.days

    form = ReceiptForm()

    if request.method == "POST":
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.status = 1
            receipt.date_warranty_to = receipt.date_purchase + relativedelta(months=receipt.lenght_of_warranty)
            receipt.save()
            return(redirect('receipt'))

        else:
            print("Form is not valid:", form.errors)

    return render(request, 'asystent_gwarancji/index.html', {'receipts':receipts, 'form':form, 'access':access})


def display_image(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)

    # Sprawdź, czy istnieje obrazek
    if receipt.image:
        # Pobierz ścieżkę do obrazka
        image_path = receipt.image.path

        # Otwórz plik obrazka i odczytaj zawartość
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Zwróć odpowiedź z zawartością obrazka
        return HttpResponse(image_data, content_type="image/jpeg")
    else:
        # Jeśli obrazek nie istnieje, zwróć odpowiedni komunikat
        return HttpResponse("Brak obrazka", status=404)

class LoginView(View):
    def get(self, request):
        # Render the login form
        form = AuthenticationForm()
        return render(request, 'asystent_gwarancji/login.html', {'form': form})

    def post(self, request):
        # Handle form submission for login
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # If the form is valid, attempt to log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # If the user is authenticated, log them in and redirect to the home page
                login(request, user)
                messages.success(request, 'Zalogowano.')
                return redirect('receipt')
            else:
                # If the user is not authenticated, display an error message
                messages.error(request, 'Błędny login lub hasło.')

        return render(request, 'asystent_gwarancji/login.html', {'form': form})

def logout_page(request):
    auth.logout(request)
    return redirect('receipt')

