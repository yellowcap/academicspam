"""Test suite for spam email parser"""

from django.test import TestCase

from django_dynamic_fixture import G
from django_mailbox.models import Message

from .models import ParseResult

###############################################################################
class ScenarioTests(TestCase):

    def test_regular_header(self):
        regular_header = """
        > From: George Bluth <george@bluth.com>
        > Subject: Fwd: There's money in the banana stand
        > Date: May 20, 2014 at 4:50:55 AM PDT
        > To: Michael Bluth <michael@bluth.com>
        """

        message = G(Message, body=regular_header)
        parseresult = G(ParseResult, message=message)
        parseresult.parse()

        self.assertEqual(parseresult.from_address, 'george@bluth.com')
        self.assertEqual(parseresult.to_address, 'michael@bluth.com')
        self.assertEqual(parseresult.subject, 'Fwd: There\'s money in the banana stand')
        self.assertEqual(parseresult.confidence, 'ok')

    def test_foreign_header(self):
        foreign_header = """
        > Remetente: George Bluth <george@bluth.com>
        > Assunto: Fwd: There's money in the banana stand
        > Data: May 20, 2014 at 4:50:55 AM PDT
        > Para: Michael Bluth <michael@bluth.com>
        """
        message = G(Message, body=foreign_header)
        parseresult = G(ParseResult, message=message)
        parseresult.parse()

        self.assertEqual(parseresult.from_address, 'george@bluth.com')
        self.assertEqual(parseresult.to_address, 'michael@bluth.com')
        self.assertEqual(parseresult.subject, 'Fwd: There\'s money in the banana stand')
        self.assertEqual(parseresult.confidence, 'ok')

    def test_multiple_to_emails_header(self):
        double_header = """
        > From: George Bluth <george@bluth.com>
        > Subject: Fwd: There's money in the banana stand
        > Date: May 20, 2014 at 4:50:55 AM PDT
        > To: Michael Bluth <michael@bluth.com>, George Michael Bluth <georgemichael@bluth.com>
        """
        message = G(Message, body=double_header)
        parseresult = G(ParseResult, message=message)
        parseresult.parse()

        self.assertEqual(parseresult.from_address, 'george@bluth.com')
        self.assertEqual(parseresult.to_address, 'michael@bluth.com')
        self.assertEqual(parseresult.subject, 'Fwd: There\'s money in the banana stand')
        self.assertEqual(parseresult.confidence, 'ok')

    def test_false_friends_header(self):
        double_header = """
        > From: George Bluth <george@bluth.a>
        > Subject: Subject: Fwd: There's money in the banana stand
        > Date: May 20, 2014 at 4:50:55 AM PDT
        > To: Michael Bluth <michael@bluth.comm>

        """
        message = G(Message, body=double_header)
        parseresult = G(ParseResult, message=message)
        parseresult.parse()

        self.assertEqual(parseresult.subject, 'Subject: Fwd: There\'s money in the banana stand')
        self.assertEqual(parseresult.confidence, 'fa')
