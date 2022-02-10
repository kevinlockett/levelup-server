from django.db import models

class Event(models.Model):    
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.TextField("event description")
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='organizing')
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")
    
    # Custom property -- To get the property on the event it’s just event.joined
    # no need for parenthesis and to use the setter: event.joined = True
    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
    