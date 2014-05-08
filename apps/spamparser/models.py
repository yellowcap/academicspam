from django.db import models

# Create your models here.

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