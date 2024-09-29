"""
tests for django models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model



class ModelTests(TestCase):

    
    def test_user_created_success(self):
        """ test if user can be created """
        
        email = "ah@example.com"
        password = "sals223"
        
        User = get_user_model()
        user = User.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_emails_are_normalized(self):
        """ test if emails are normalized"""
        emails = [
            ['test@Example.com', 'test@example.com'],
            ['test16@ExAMPLE.com', 'test16@example.com'],
            ['teSt@Example.COM', 'teSt@example.com'],
            ['Test@Example.com', 'Test@example.com'],
        ]

        for email, expected in emails:
            user = get_user_model().objects.create_user(email, "asasafe")
            self.assertEqual(user.email, expected)

    def test_user_raises_error_with_empty_email(self):
        """ test to raise error if no email passed when creating a user """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "12354sas")

    def test_create_superuser(self):
        """ test creating super user """
        email = "ah@example.com"
        password = "sals223"
        
        User = get_user_model()
        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)