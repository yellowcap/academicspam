"""Models for handling metadata connected to email spam"""

import re

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django_mailbox.models import Message

###############################################################################
class Publisher(models.Model):
    website = models.URLField()

    def __unicode__(self):
        return self.website

class Sender(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email

class Recipient(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email

class Spam(models.Model):
    subject = models.CharField(max_length=100)
    sender = models.ForeignKey(Sender)
    recipient = models.ForeignKey(Recipient)
    publisher = models.ForeignKey(Publisher)
    filename = models.CharField(max_length=100)

    def __unicode__(self):
        return self.subject

class ParseResult(models.Model):
    """
    Model to store results from parsing spam emails. This includes original
    from and to email addresses, and the original subject.
    """
    CONFIDENCE_LEVELS = (
        ('no', 'Not parsed yet'),
        ('fa', 'Failed'),
        ('ok', 'Success')
    )
    message = models.OneToOneField(Message)
    from_address = models.EmailField(null=True, blank=True)
    to_address = models.EmailField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    confidence = models.CharField(max_length=2, choices=CONFIDENCE_LEVELS, default='no')
    
    def __unicode__(self):
        return self.subject

    def parse(self):
        """Method that parses original email and stores results in model"""
        # Get email body string
        msg = self.message.get_text_body()

        # Email line candidates
        email_line_finder = re.compile('.*:.*<.*@.*\..*>.*', re.IGNORECASE)
        
        # Email in brackets <abc@abc.com>
        email_finder = re.compile('<[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}>', re.IGNORECASE)
        
        # Last word in string
        category_finder = re.compile('\w+$', re.IGNORECASE) 
        
        # List of konwn from/to prefixes
        known_froms = ['from', 'remetente']
        known_tos = ['to', 'para']

        # Get all email line candidates
        email_lines = email_line_finder.findall(msg)
        
        for line in email_lines:
            # Parse email address
            email = email_finder.findall(line)
            if len(email):
                email = email[0][1:-1]
                # If email address is not valid, skip line
                if not self.validate_email(email):
                    continue

            # Parse category
            category = line.split(':')[0]
            category = category_finder.findall(category)
            
            # Match category with known keywords
            if len(category):
                category = category[0].lower()
                if category in known_froms:
                    self.from_address = email
                elif category in known_tos:
                    self.to_address = email

        # Subject
        known_subjects = ['subject', 'assunto']
        pattern = ''
        for subj in known_subjects:
            pattern += '( ' + subj + ':.*)|'
        pattern = pattern[:-1]
        subject_line_finder = re.compile(pattern, re.IGNORECASE)
        subject_lines = subject_line_finder.findall(msg)
        
        for subj in subject_lines:
            subj = [x for x in subj if x != ''][0]
            subj = subj.split(':')[1:]
            subj = ':'.join(subj).strip()
            self.subject = subj

        # Confidence
        if self.from_address and self.to_address and self.subject:
            self.confidence = 'ok'
        else:
            self.confidence = 'fa'
        
        self.save()

    def validate_email(self, email):
        """Method using django email validator to check email strings"""
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

