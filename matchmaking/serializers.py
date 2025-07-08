from rest_framework import serializers
from .models import Match
from .models import MatchRequest, Match
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
     #   read_only_fields = ['team_b', 'status', 'created_at']
    read_only_fields = [ 'status', 'created_at']



class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRequest
        fields = ['id', 'team_a', 'team_b', 'mode', 'status', 'created_at']
    read_only_fields = ['status', 'created_at']
