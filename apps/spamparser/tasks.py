"""Celery tasks for periodic email parsing"""

from celery import shared_task

from django_mailbox.models import Mailbox, Message

###############################################################################
@shared_task
def get_email(name='get_email'):
    """Retrieve email from IMAP account using django-mailbox"""
    for mailbox in Mailbox.objects.all():
        mailbox.get_new_mail()

@shared_task
def parse_email(name='parse_email'):
    """Parse all non-parsed emails"""
    for msg in Message.objects.filter(confidence='no'):
        msg.parse()
