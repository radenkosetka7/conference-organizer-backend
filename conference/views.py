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
        serializer.save(creator=self.request.user)


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


class ReservedItemsAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReservedItemSerializer

class ReservedItemsChangeAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReservedItemChangeSerializer


class EventVisitorCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventVisitorCreateSerializer


class EventVisitorDeleteAPIView(DestroyAPIView):
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
        queryset= Conference.objects.filter(events__eventvisitor__visitor=user).distinct()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = Conference.objects.filter(start__range=(start_date, end_date))

        return queryset
