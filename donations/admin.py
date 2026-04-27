from django.contrib import admin
from .models import Donacion

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'monto', 'estado', 'referencia', 'fecha')
    list_filter = ('estado',)
    search_fields = ('nombre', 'referencia')