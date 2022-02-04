from django.db import models

class Game(models.Model):
    title = models.CharField("game title", max_length=100)
    maker = models.CharField("game maker", max_length=100)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, verbose_name='the related game type',)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, verbose_name='gamer associated with this game',)