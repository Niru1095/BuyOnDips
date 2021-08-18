from django.contrib import admin
from .models import StockNames
# Register your models here.

class StockNamesAdmin(admin.ModelAdmin):
    list_display = ['symbol','companyName']
    search_fields = ['symbol','companyName']
    readonly_fields = ['symbol','companyName']

admin.site.register(StockNames,StockNamesAdmin)