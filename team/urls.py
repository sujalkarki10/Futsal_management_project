from django.urls import path
from .views import team_list

from .views import TeamDetail
from .views import PlayerDetail



urlpatterns = [
    path('', team_list),
path('<int:pk>/', TeamDetail.as_view()),         # GET/PUT/DELETE team by ID
    path('player/<int:pk>/', PlayerDetail.as_view()), # GET/PUT/DELETE player by ID
    path('players/<int:team_id>/', PlayerDetail.add_players_to_team)
    ]
