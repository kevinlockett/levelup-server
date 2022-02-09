from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType

class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = CreateGameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        
        # The next 3 lines filter games by game type
        game_type = request.query_params.get('type', None) #request.query_params is a dictionary of any query params in the url
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
    
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#        # retrieve gameType object from the dbase to make sure it really exists; data retrieved is held in request.data dictionary.
#        game_type = GameType.objects.get(pk=request.data["game_type"])


#        # call "create" ORM (Object Relational Mapping) as pass fields as parameters to the function
#        game = Game.objects.create(
#            title=request.data["title"],
#            maker=request.data["maker"],
#            number_of_players=request.data["number_of_players"],
#            skill_level=request.data["skill_level"],
#            gamer=gamer,
#            game_type=game_type
#        )

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

#        # created object is now serialized into dictionary version for json and returned to client
#        serializer = GameSerializer(game)
#        return Response(serializer.data)

#    def update(self, request, pk):
#        """Handle PUT requests for a game

#        Returns:
#            Response -- Empty body with 204 status code
#        """
#        game = Game.objects.get(pk=pk)
#        game.title = request.data["title"]
#        game.maker = request.data["maker"]
#        game.number_of_players = request.data["number_of_players"]
#        game.skill_level = request.data["skill_level"]
#        game.game_type = GameType.objects.get(pk=request.data["game_type"])
#        game.save()

#        return Response(status=status.HTTP_204_NO_CONTENT)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        # fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type_id', 'gamer_id')
        fields = '__all__'
        depth = 1 # adds depth to serializer to embed nested data -- in this case game type and gamer
        
class CreateGameSerializer(serializers.ModelSerializer):
    """JSON serializer for adding new games
    """
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']