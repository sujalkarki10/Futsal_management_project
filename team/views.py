from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Team
from .serializers import TeamSerializer

from rest_framework import generics, permissions
from .models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def team_list(request):
    if request.method == 'GET':
        teams = Team.objects.filter(manager=request.user)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['manager'] = request.user.id  # ✅ Set manager
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(manager=self.request.user)

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(team__manager=self.request.user)

    @api_view(['POST'])
    def add_players_to_team(request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if isinstance(data, list):
            for item in data:
                item['team'] = team.id  # add team reference to each
            serializer = PlayerSerializer(data=data, many=True)
        else:
            serializer = PlayerSerializer(data=data)

        if serializer.is_valid():
            serializer.save(team=team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


