from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'event_type'

    def __str__(self):
        return self.name


class Conference(models.Model):
    name = models.CharField(max_length=45)
    url = models.CharField(max_length=45, null=True, blank=True)
    finished = models.SmallIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_conferences')
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    rating = models.ManyToManyField(User, through='Rating')

    class Meta:
        db_table = 'conference'
        ordering = ['name']

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='ratings')
    stars = models.SmallIntegerField(null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField()

    class Meta:
        db_table = 'rating'

    def __str__(self):
        return self.stars + " " + self.comment + " " + self.date


class ResourceItem(models.Model):
    name = models.CharField(max_length=45)
    number = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='resource_items')

    class Meta:
        db_table = 'resource_item'

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='rooms')

    class Meta:
        db_table = 'room'

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=45)
    start = models.DateTimeField()
    end = models.DateTimeField()
    finished = models.SmallIntegerField()
    url = models.CharField(max_length=45, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    event_type = models.ForeignKey(EventType, models.DO_NOTHING)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='events')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_moderator', default=None)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.name


class EventVisitor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event_visitor'

class ReservedItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    resource_item = models.ForeignKey(ResourceItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'reserved_item'


