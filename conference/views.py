from django.shortcuts import render
from rest_framework.generics import *
from .models import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializer import *
# Create your views here.


class EventTypeAPIView(ListAPIView):
    queryset = EventType.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventTypeSerializer


class ResourceItemAPIView(UpdateAPIView):
    queryset = ResourceItem.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ResourceItemSerializer


class RoomAPIView(UpdateAPIView):
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RoomSerializer

class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer

class LocationAPIView(UpdateAPIView):
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationItemSerializer


class ConferenceListAPIView(ListAPIView):
    queryset = Conference.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        creator_id=self.kwargs['creator_id']
        return self.request.filter(creator_id=creator_id)


class ConferenceCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceItemSerializer

class ConferenceAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Conference.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return ConferenceItemSerializer
        return ConferenceSerializer

class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

class EventCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventItemSerializer

class EventAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return EventItemSerializer
        return EventSerializer

class RatingAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingItemSerializer


class ConferenceSearchView(ListAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=Conference.objects.all()
        search_query=self.request.query_params.get('search_query')
        if search_query:
            queryset=queryset.filter(name__icontains=search_query)
        return queryset

class ConferenceFilterView(ListAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=Conference.objects.all()
        finished = self.request.query_params.get('finished')
        start_min = self.request.query_params.get('start_min')
        start_max = self.request.query_params.get('start_max')
        url_not_null = self.request.query_params.get('url_not_null')
        url_null = self.request.query_params.get('url_null')

        if finished is not None:
            queryset = queryset.filter(finished=finished == 'true')

        if start_min:
            queryset = queryset.filter(start__gte=start_min)

        if start_max:
            queryset = queryset.filter(start__lte=start_max)

        if url_not_null:
            queryset = queryset.exclude(url=None)

        if url_null:
            queryset = queryset.filter(url=None)

        return queryset

