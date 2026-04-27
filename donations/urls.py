from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aprobar-donacion/<str:referencia>/', views.aprobar_donacion, name='aprobar_donacion')
]