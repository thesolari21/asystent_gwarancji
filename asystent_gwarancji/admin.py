from django.contrib import admin

# Register your models here.

from .models import Receipt

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'date_purchase', 'date_warranty_to', 'status')
    list_filter = ( 'name', 'date_purchase', 'date_warranty_to', 'status')

admin.site.register(Receipt, ReceiptAdmin)