from django.urls import path
from . import views
from .views import LoginView

urlpatterns = [
    path('', views.receipt, name='receipt'),
    path('image/<int:receipt_id>/', views.display_image, name='display_image'),
    path('logout', views.logout_page, name='logout_page'),
    path('login/', LoginView.as_view(), name='login_page'),





]
