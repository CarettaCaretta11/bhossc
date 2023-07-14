"""
Tests for models.
"""
import time
from unittest.mock import patch
from decimal import Decimal
from time import sleep

from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models


def create_user(email='user@example.com', password='samplepass123'):
    """ Create and return a test user. """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """ Test models. """

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful. """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test email is normalized for new users. """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@examplE.com', 'Test2@example.com'],
            ['TEST3@ExAmPle.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'samplepass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test that creating a user without an email raises a ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'samplepass123')

    def test_create_superuser(self):
        """ Test creating a superuser. """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'samplepass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_room(self):
        """ Test creating a room is successful. """
        user = get_user_model().objects.create_user(
            'test@example.com',
            'samplepass123',
        )
        room = models.Room.objects.create(
            host=user,
            name='Sample room',
            description='Sample description.',
            topic='Testing',
        )

        self.assertEqual(str(room), room.name)

        time.sleep(5)
        self.assertAlmostEqual(room.get_time_diffr() == 5)

    def test_create_topic(self):
        """ Test creating a topic is successful. """
        user = create_user()
        topic = models.Topic.objects.create(name='Testing')

        self.assertEqual(str(topic), topic.name)

    def test_create_message(self):
        """ Test creating a message is successful. """
        user = create_user()
        room = models.Room.objects.create(
            host=user,
            name='Sample room',
            description='Sample description.',
            topic='Testing',
        )
        message = models.Message.objects.create(
            user=user,
            room=room,
            body='Sample message',
        )

        self.assertEqual(str(message), message.body[:10])
