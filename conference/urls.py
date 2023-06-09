from django.urls import path

from conference.views import EventTypeAPIView, ResourceItemAPIView, LocationListAPIView, \
    ConferenceListAPIView, ConferenceCreateAPIView, ConferenceAPIView, EventAPIView, EventListAPIView, \
    EventCreateAPIView, RatingAPIView, ReservedItemsAPIView, EventVisitorCreateAPIView, UserEventsListView, \
    ConferenceListModeratorAPIView, ConferenceListOraganizerAPIView, ReservedItemsChangeAPIView, \
    EventVisitorDeleteAPIView, VisitorRetrieveAPIView

urlpatterns = [
    path('event_types/', EventTypeAPIView.as_view(), name='event_type_list'),
    #path('rooms/<int:pk>', RoomAPIView.as_view(), name='rooms'),
    path('resource_items/<int:pk>', ResourceItemAPIView.as_view(), name='items'),
    path('locations/list/', LocationListAPIView.as_view(), name='locations_list'),
    #path('locations/<int:pk>', LocationAPIView.as_view(), name='location'),
    path('conferences/list/', ConferenceListAPIView.as_view(), name='conferences_list'),
    path('conferences/', ConferenceCreateAPIView.as_view(), name='conference_create'),
    path('conferences/<int:pk>', ConferenceAPIView.as_view(), name='conference_crud'),
    path('events/<int:pk>', EventAPIView.as_view(), name='event_crud'),
    path('events/list/', EventListAPIView.as_view(), name='events_list'),
    path('events/', EventCreateAPIView.as_view(), name='event_create'),
    path('rating/', RatingAPIView.as_view(), name='rating_create'),
    path('reserved_items/', ReservedItemsAPIView.as_view(), name='reserved_items'),
    path('reserved_items/<int:pk>',ReservedItemsChangeAPIView.as_view(),name='reserved_items_change'),
    path('event-visitors/', EventVisitorCreateAPIView.as_view(), name='event-visitors-create'),
    path('event-visitors/<int:pk>', EventVisitorDeleteAPIView.as_view(), name='event-visitors-delete'),
    path('user_events/', UserEventsListView.as_view(), name='user_events_list'),
    path('conferences/moderator/', ConferenceListModeratorAPIView.as_view(), name='conferences_moderator'),
    path('conferences/organizer/', ConferenceListOraganizerAPIView.as_view(), name='conferences_organizer'),
    path('visitor/', VisitorRetrieveAPIView.as_view(), name='visitor-retrieve'),

]
