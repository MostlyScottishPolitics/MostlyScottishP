__author__ = 'laura'

from django.test import TestCase

from msp.models import *

#insert unit tests here


class PartyTestCase(TestCase):
    """
    test cases for Party
    """
    def setUp(self):
        Party.objects.create(id=1, name="party")
        Party.objects.create(id=1, name="politics", description="greatest party ofc")

    def test_party(self):
        p1 = Party.objects.get(id=1)
        p2 = Party.objects.get(id=2)
        self.assertEqual(p1.name, 'party')
        self.assertEqual(p2.category, 'politics')