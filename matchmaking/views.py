from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Match, MatchRequest
from .serializers import MatchSerializer

from .utils import generate_smart_fixtures

from .serializers import MatchRequestSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def match_list_create(request):
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_fixtures_view(request):
    generate_smart_fixtures()
    return Response({"message": "Fixtures generated successfully"}, status=status.HTTP_201_CREATED)






from team.models import Team


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_friendly_match(request):
    user = request.user
    team_a_id = request.data.get('team_a')
    team_b_id = request.data.get('team_b')

    # --- Validate input ---
    if not team_a_id or not team_b_id:
        return Response({'error': 'Both team_a and team_b are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if team_a_id == team_b_id:
        return Response({'error': 'Cannot create a match between the same team.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team_a = Team.objects.get(id=team_a_id)
        team_b = Team.objects.get(id=team_b_id)
    except Team.DoesNotExist:
        return Response({'error': 'One or both team IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)

    # --- Enforce ownership rule ---
    if team_a.manager != user:
        return Response({'error': 'You can only request a match from a team you own.'}, status=status.HTTP_403_FORBIDDEN)

    if team_b.manager == user:
        return Response({'error': 'You cannot request a friendly match with your own team.'}, status=status.HTTP_400_BAD_REQUEST)

    # --- Create the match ---
    match = MatchRequest.objects.create(
        team_a=team_a,
        team_b=team_b,
        mode='friendly',
        status='pending'
    )

    return Response({
        "message": "Friendly match request created.",
        "request_id": match.id
    }, status=status.HTTP_201_CREATED)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_request(request, request_id):
    try:
        match_request = MatchRequest.objects.get(id=request_id)
    except MatchRequest.DoesNotExist:
        return Response({"error": "Request not found."}, status=404)

    action = request.data.get("action")
    if action not in ['accept', 'reject']:
        return Response({"error": "Invalid action."}, status=400)

    if action == 'accept':
        match_request.status = 'accepted'
        match_request.save()

        # Create actual match record
        Match.objects.create(
            team_a=match_request.team_a,
            team_b=match_request.team_b,
            mode='friendly',
            status='pending'
        )

        return Response({"message": "Request accepted and match created."})

    else:
        match_request.status = 'rejected'
        match_request.save()
        return Response({"message": "Request rejected."})

