from django.shortcuts import render_to_response
import os, email, re
from email_counter.models import Publisher, Sender, Recipient, Spam

path = '/Users/john/Local sites/Maildir/Maildir/new'

def update_email_db():

    files = os.listdir(path)
    email_files = [i for i in files if i[-9:] == 'signature']
    for i in email_files:
        # first check that this email has not been entered in database
        #if Spam.objects.filter(filename=i).exists():
        if False:
            # skip this one
            continue
        else:
            headers = parse_email(i)
            try:
                sender = headers['sender']
            except:
                sender = ''
            s = Sender(email=sender)
            s.save()
            try:
                recipient = headers['recipient']
            except:
                recipient = ''
            r = Recipient(email=recipient)
            r.save()
            try:
                website = headers['sender'][1].split('@')[1]
            except:
                website = ''
            p = Publisher(website=website)
            p.save()
            new_entry = Spam(subject=headers['subject'], filename=headers['filename'], sender=s, recipient=r, publisher=p)
            new_entry.save()

def parse_email(email_file):
    email_filename = os.path.join(path, email_file)
    raw_email = open(email_filename).read()
    message = email.message_from_string(raw_email)

    # grab info from the email
    try:
        subject = message['subject']
    except:
        subject = ''
    try:
        recipient = message['from']
    except:
        recipient = ''
    # Now the hard part. Find the spammer's email address!
    publisher = ''
    if message.is_multipart():
        # find the body with fwd'ed headers among the payloads
        for payload in message.get_payload():
            text = payload.get_payload()
            try:
                candidate = re.search('From:\s(.*)\n', text).group(1)
                publisher = email.utils.parseaddr(candidate)
                break
            except:
                continue
    else:
        # this is just a plaintext message
        text = message.get_payload()
        try:
            candidate = re.search('From:\s(.*)\n', text)
            publisher = email.utils.parseaddr(candidate)
        except:
            pass
    return {'subject':subject, 'recipient':recipient, 'publisher':publisher, 'filename':email_file}

def index(request):
    update_email_db()
    return render_to_response('index.html', {'data':Spam.objects.all()})