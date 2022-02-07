from re import I
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer

class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        
        #the next 3 lines filter events by game
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # getting the gamer that is logged in using the user's auth token
        organizer = Gamer.objects.get(user=request.auth.user)
        
        # retrieve game object from the dbase to make sure it really exists; data retrieved is held in request.data dictionary.
        game = Game.objects.get(pk=request.data["game"])
        
        try:
            serializer = CreateEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(organizer=organizer)
            serializer.save(game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        # fields = ('id', 'description', 'date', 'time', 'game_id')
        fields = '__all__'
        depth = 2
        
class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for adding new games
    """
    class Meta:
        model = Event
        fields = ['id', 'description', 'date', 'time', 'game', 'organizer']