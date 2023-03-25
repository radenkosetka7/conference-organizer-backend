from rest_framework import serializers

from conference.models import *
from users.serializer import UserIdentity


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model=EventType
        fields='__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model=Room
        fields=('name','description','event')


class ResourceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=ResourceItem
        fields=('name','number','price')

class LocationSerializer(serializers.ModelSerializer):

    rooms=RoomSerializer(many=True)
    resource_items=ResourceItemSerializer(many=True)
    class Meta:
        model=Location
        fields='__all__'

class LocationItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Location
        fields=('id','name','address','occupied')

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model=User
        fields=('username','first_name','last_name')



class EventSerializer(serializers.ModelSerializer):

    location=LocationSerializer()
    event_type=EventTypeSerializer()
    attendees=UserSerializer(many=True,read_only=True)
    class Meta:
        model=Event
        fields=('name','start','end','finished','url','attendees')

class EventItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Event
        fields=('name','start','end','finished','url','conference','event_type','location')

class RatingSerializer(serializers.ModelSerializer):

    username=UserSerializer(read_only=True)
    class Meta:
        model=Rating
        fields=('stars','comment','date')

class RatingItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Rating
        fields=('stars','comment','date','user','conference')

class ConferenceSerializer(serializers.ModelSerializer):

    location=LocationSerializer()
    events=EventSerializer(many=True)
    ratings=RatingSerializer(many=True,read_only=True)
    class Meta:
        model=Conference
        fields=('name','start','end','finished','url')


class ConferenceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Conference
        fields=('name','start','end','finished','url','creator','location')

