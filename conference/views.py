from django.shortcuts import render
from rest_framework.generics import *
from .models import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializer import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# Create your views here.


class EventTypeAPIView(ListAPIView):
    queryset = EventType.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventTypeSerializer


class ResourceItemAPIView(UpdateAPIView):
    queryset = ResourceItem.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ResourceItemSerializer


class RoomAPIView(UpdateAPIView):
    queryset = Room.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RoomSerializer

class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LocationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class LocationAPIView(UpdateAPIView):
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationItemSerializer


class ConferenceListAPIView(ListAPIView):
    queryset = Conference.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ConferenceSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend]
    filterset_fields = ['start', 'end', 'finished','url']
    search_fields = ['name']



class ConferenceCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConferenceItemSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ConferenceAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Conference.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ConferenceItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return ConferenceItemSerializer
        return ConferenceSerializer

class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

class EventCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventItemSerializer

class EventAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return EventItemSerializer
        return EventSerializer

class RatingAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RatingItemSerializer

class ReservedItemsAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ReservedItemSerializer

class EventVisitorCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

class UserEventsListView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(visitors=user)
