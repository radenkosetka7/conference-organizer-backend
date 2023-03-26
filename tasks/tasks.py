from celery import shared_task
from django.utils import timezone

from conference.models import Conference, Event, Room, Location


@shared_task
def update_conference_status():
    now = timezone.now()
    for conference in Conference.objects.filter(is_finished=False):
        if now >= conference.end:
            conference.is_finished = True
            conference.save()


@shared_task
def update_event_status():
    now = timezone.now()
    for event in Event.objects.filter(is_finished=False):
        if now >= event.end:
            event.is_finished = True
            event.save()


        if event.url:
            room=Room.objects.filter(event=event).first()
            if room:
                room.event=None
                room.save()

            for reserved_item in event.reserved_items.all():
                reserved_item.resource_item.number += reserved_item.quantity
                reserved_item.resource_item.save()

                reserved_item.delete()


@shared_task
def update_occupied_status():
    locations = Location.objects.all()
    for location in locations:
        rooms = location.rooms.all()
        occupied = all(room.event is not None for room in rooms)
        if occupied != location.occupied:
            location.occupied = occupied
            location.save()

