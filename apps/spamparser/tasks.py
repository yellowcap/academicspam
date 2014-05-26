"""Celery tasks for periodic email parsing"""

from celery import shared_task

from django_mailbox.models import Mailbox

###############################################################################
@shared_task
def get_email(name='get_email'):
    """Retrieve email from IMAP account using django-mailbox"""
    for mailbox in Mailbox.objects.all():
        mailbox.get_new_mail()
