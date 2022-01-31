from django.db import models

class GameType(models.Model):
    label = models.CharField("game type", max_length=50)
