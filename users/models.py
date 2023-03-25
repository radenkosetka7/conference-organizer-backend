from django.db import models

# Create your models here.


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def user_status_changed(sender, instance, created, **kwargs):
    if not created and instance.is_active:
        send_mail(
            'Vaš račun je aktiviran',
            'Poštovani {0},\n\nVaš račun je sada aktivan.\n\nHvala Vam što koristite našu aplikaciju.'.format(instance.first_name),
            'noreply@example.com',
            [instance.email],
            fail_silently=False,
        )