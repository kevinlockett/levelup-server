from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
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
            serializer = CreateEventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.all()
        
        #the next 3 lines filter events by game
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
            
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # getting the gamer that is logged in using the user's auth token
        gamer = Gamer.objects.get(user=request.auth.user)
        
        # retrieve game object from the dbase to make sure it really exists; data retrieved is held in request.data dictionary.
        game = Game.objects.get(pk=request.data["game"])

        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)
        serializer.save(game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
#    def update(self, request, pk):
#        """Handle PUT requests for an event

#        Returns:
#            Response -- Empty body with 204 status code
#        """
#        event = Event.objects.get(pk=pk)
#        event.description = request.data["description"]
#        event.date = request.data["date"]
#        event.time = request.data["time"]
#        event.game = Game.objects.get(pk=request.data['game'])
#        event.save()

#        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user from an event"""
        
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed from attendee list'}, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer', 'description', 'date', 'time', 'attendees', 'joined')
        depth = 1
        
class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for adding new games
    """
    class Meta:
        model = Event
        fields = ['id', 'description', 'date', 'time', 'game']