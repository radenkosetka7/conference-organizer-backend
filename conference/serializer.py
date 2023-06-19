from rest_framework import serializers

from conference.models import *
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.serializer import UserIdentity


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'description')


class ResourceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceItem
        fields = ('id', 'name', 'number', 'price')


class LocationSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)
    resource_items = ResourceItemSerializer(many=True)

    class Meta:
        model = Location
        fields = '__all__'


class LocationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'address')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class ResourceItemNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceItem
        fields = ('id', 'name', 'number',)


class ReservedItemGetSerializer(serializers.ModelSerializer):
    resource_item = ResourceItemNameSerializer()

    class Meta:
        model = ReservedItem
        fields = ('id', 'resource_item', 'quantity')


class EventVisitorGetSerializer(serializers.ModelSerializer):
    visitor = UserSerializer()

    class Meta:
        model = EventVisitor
        fields = ('id', 'visitor')


class EventSerializer(serializers.ModelSerializer):
    location = LocationItemSerializer()
    event_type = EventTypeSerializer()
    reserved_items = ReservedItemGetSerializer(many=True, source='reserveditem_set')
    event_visitors = EventVisitorGetSerializer(many=True, source='eventvisitor_set')
    moderator = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'finished', 'url', 'moderator', 'room', 'event_type', 'location',
                  'event_visitors', 'reserved_items')


class EventItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'url', 'conference', 'event_type', 'location', 'moderator', 'room')


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rating
        fields = ('stars', 'comment', 'date', 'user')


class RatingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'comment', 'conference')


class ReservedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedItem
        fields = ('id', 'event', 'resource_item', 'quantity')

    def create(self, validated_data):
        quantity = validated_data['quantity']
        resource_item = validated_data['resource_item']
        resource_item.number -= quantity
        resource_item.save()
        reserved_item = ReservedItem.objects.create(**validated_data)
        return reserved_item


class ReservedItemChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedItem
        fields = ('id', 'event', 'resource_item', 'quantity')

    def update(self, instance,validated_data):
        item = self.instance.quantity
        quantity = validated_data['quantity']
        resource_item = validated_data['resource_item']
        resource_item.number += item
        resource_item.number -= quantity
        resource_item.save()
        instance.quantity=quantity
        instance.save()
        return instance


class ConferenceSerializer(serializers.ModelSerializer):
    location = LocationItemSerializer()
    events = EventSerializer(many=True)
    ratings = RatingSerializer(many=True, read_only=True)
    creator = UserSerializer()

    class Meta:
        model = Conference
        fields = ('id', 'name', 'start', 'end', 'finished', 'creator', 'url', 'location', 'events', 'ratings')


class ConferenceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('id', 'name', 'start', 'end', 'url', 'location','finished')


class EventVisitorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVisitor
        fields = ('id', 'event', 'visitor')


class EventVisitorDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVisitor
        fields = ('id', 'event', 'visitor')


class EventModeratorSerializer(serializers.ModelSerializer):
    location = LocationItemSerializer()
    event_type = EventTypeSerializer()
    reserved_items = ReservedItemGetSerializer(many=True, source='reserveditem_set')
    event_visitors = EventVisitorGetSerializer(many=True, source='eventvisitor_set')
    room = RoomSerializer()

    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'finished', 'url', 'room', 'event_type', 'location',
                  'event_visitors', 'reserved_items')

    @receiver(pre_delete, sender=Event)
    def edit_reserved_items(sender, instance, **kwargs):
        if instance.finished == 0:
            reserved_items = instance.reserveditem_set.all()
            for reserved_item in reserved_items:
                resource_item = reserved_item.resource_item
                resource_item.number += reserved_item.quantity
                resource_item.save()




class EventVisitorSerializer(serializers.ModelSerializer):
    location = LocationItemSerializer()
    event_type = EventTypeSerializer()
    reserved_items = ReservedItemGetSerializer(many=True, source='reserveditem_set')
    event_visitors = EventVisitorGetSerializer(many=True, source='eventvisitor_set')
    moderator = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'finished', 'url', 'moderator', 'room', 'event_type', 'location',
                  'reserved_items','event_visitors')


class ConferenceVisitorSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    location = LocationItemSerializer()
    ratings = RatingSerializer(many=True, read_only=True)
    creator = UserSerializer()

    class Meta:
        model = Conference
        fields = ('id', 'name', 'start', 'end', 'finished', 'creator', 'url', 'location', 'events', 'ratings')

    def get_events(self, conference):
        user = self.context['request'].user
        events = conference.events.filter(eventvisitor__visitor=user)
        serializer = EventVisitorSerializer(events, many=True)
        return serializer.data


class ConferenceModeratorSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    location = LocationItemSerializer()
    ratings = RatingSerializer(many=True, read_only=True)
    creator = UserSerializer()

    class Meta:
        model = Conference
        fields = ('id', 'name', 'start', 'end', 'finished', 'creator', 'url', 'location', 'events', 'ratings')

    def get_events(self, conference):
        user = self.context['request'].user
        moderator_events = conference.events.filter(moderator=user)
        serializer = EventModeratorSerializer(moderator_events, many=True)
        return serializer.data

