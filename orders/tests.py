from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Address


class OrdersViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="orderviewer",
            email="orderviewer@example.com",
            password="strong-pass-123",
        )
        self.client.force_login(self.user)

    def test_order_history_page_renders_professionally(self):
        response = self.client.get(reverse("order_view"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order history")
        self.assertContains(response, "Your recent purchases")


class CheckoutViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            email="tester@example.com",
            password="strong-pass-123",
        )
        self.client.force_login(self.user)

    def test_checkout_shows_saved_addresses_and_add_address_prompt(self):
        Address.objects.create(
            user=self.user,
            full_name="Jane Doe",
            phone="9800000000",
            line1="123 Main Street",
            line2="",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            country="India",
        )

        response = self.client.get(reverse("checkout"))

        self.assertIn("addresses", response.context)
        self.assertEqual(len(response.context["addresses"]), 1)
        self.assertContains(response, "Choose this address")
        self.assertContains(response, "Add a new address")

    def test_checkout_shows_prompt_when_no_address_is_saved(self):
        response = self.client.get(reverse("checkout"))

        self.assertContains(response, "No delivery address yet")
        self.assertContains(response, "Add a new address")
