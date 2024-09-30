"""
tests for django admin modifications
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):

    def setUp(self):
        """ create user and client """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@g.com",
            password="abc123"
        )
        self.user = get_user_model().objects.create_user(
            email="user@g.com",
            password="abc123",
            name="User"
        )
        self.client.force_login(self.admin_user)
    
    def test_users_list(self):
        """ test that users are listed on page """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ test that the user edit page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user(self):
        """ test the create user page """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)