# C:\Users\Admin\connect_website\collaborate\tests.py
from django.test import TestCase
from .models import Idea

class IdeaModelTest(TestCase):
    def test_string_representation(self):
        idea = Idea(title="Test Idea")
        self.assertEqual(str(idea), "Test Idea")
