from django.urls import path
from . import views

urlpatterns = [

     path('', views.match_list_create),
    path('generate-fixtures/', views.generate_fixtures_view),
    path('friendly/request/', views.create_friendly_match  ),
    path('friendly/respond/<int:request_id>/', views.respond_to_request),
]
