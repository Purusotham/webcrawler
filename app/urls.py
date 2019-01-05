from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('parse_html', views.parse_html, name="index")
]