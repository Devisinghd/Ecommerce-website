from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="profileviewer",
            email="profileviewer@example.com",
            password="strong-pass-123",
        )
        self.client.force_login(self.user)

    def test_profile_view_renders_profile_page(self):
        response = self.client.get(reverse("profile-view", kwargs={"id": self.user.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile overview")
