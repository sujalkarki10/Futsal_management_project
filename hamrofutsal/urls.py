from django.urls import path
from .import views

urlpatterns = [
    path('new/',views.new, name="new1"),
    path('', views.index, name ="index"),
]