from datetime import datetime

from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# Create your views here.


class EventTypeAPIView(ListAPIView):
    queryset = EventType.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventTypeSerializer


class ResourceItemAPIView(UpdateAPIView):
    queryset = ResourceItem.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ResourceItemSerializer


# class RoomAPIView(UpdateAPIView):
#     queryset = Room.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = RoomSerializer


class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


# class LocationAPIView(UpdateAPIView):
#     queryset = Room.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = LocationItemSerializer


class ConferenceListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['finished']
    search_fields = ['name']

    def get_queryset(self):
        queryset = Conference.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = Conference.objects.filter(start__range=(start_date, end_date))

        queryset = queryset.exclude(finished=3)

        return queryset


class ConferenceListModeratorAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceModeratorSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['finished']
    search_fields = ['name']

    def get_queryset(self):
        user=self.request.user
        queryset= Conference.objects.filter(events__moderator=user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = Conference.objects.filter(start__range=(start_date, end_date))

        return queryset


class ConferenceListOraganizerAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['finished']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        queryset = Conference.objects.filter(creator=user)
        return queryset


class ConferenceCreateAPIView(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ConferenceItemSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user,finished=0)


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

    def perform_create(self, serializer):
        serializer.save(finished=0)


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,date=datetime.now())


class ReservedItemsAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReservedItemSerializer

class ReservedItemsChangeAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ReservedItem.objects.all();
    permission_classes = (IsAuthenticated,)
    serializer_class = ReservedItemChangeSerializer


class EventVisitorCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventVisitorCreateSerializer


class EventVisitorDeleteAPIView(DestroyAPIView):
    queryset = EventVisitor.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EventVisitorDeleteSerializer
class UserEventsListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConferenceVisitorSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['finished']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        queryset= Conference.objects.filter(events__eventvisitor__visitor=user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = Conference.objects.filter(start__range=(start_date, end_date))

        return queryset


class VisitorRetrieveAPIView(ListAPIView):
    queryset = EventVisitor.objects.all()
    serializer_class = EventVisitorGetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        event = self.request.query_params.get('event')
        visitor = self.request.query_params.get('visitor')
        queryset=EventVisitor.objects.filter(event=event, visitor=visitor)
        return queryset
