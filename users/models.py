from django.db import models

# Create your models here.


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail


# @receiver(post_save, sender=User)
# def user_status_changed(sender, instance, created, **kwargs):
#     if not created and instance.is_active:
#         send_mail(
#             'Your account is now active',
#             'Respected {0},\n\n Your account is now active.\n\nThank You for using our application.'.format(
#                 instance.first_name),
#             'noreply@example.com',
#             [instance.email],
#             fail_silently=False,
#         )
