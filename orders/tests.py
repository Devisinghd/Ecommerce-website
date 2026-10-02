from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from myapp.models import Products
from .models import Address, Order, OrderItem


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
        self.product = Products.objects.create(
            seller=self.user,
            name='Checkout watch',
            price=125,
            description='Test product',
            image='images/checkout-watch.jpg',
            stock=5,
        )

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

    def test_checkout_creates_order_with_address_and_clears_cart(self):
        address = Address.objects.create(
            user=self.user,
            full_name='Jane Doe',
            phone='9800000000',
            line1='123 Main Street',
            line2='',
            city='Mumbai',
            state='Maharashtra',
            postal_code='400001',
            country='India',
        )
        session = self.client.session
        session['cart'] = {str(self.product.id): {'price': str(self.product.price), 'qty': 2}}
        session.save()

        response = self.client.post(reverse('checkout'), {'selected_address_id': address.id})

        self.assertRedirects(response, reverse('order-success'))
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.delivery_address, address)
        self.assertEqual(order.total_amount, 250)
        self.assertEqual(OrderItem.objects.get(order=order).quantity, 2)
        self.assertEqual(self.client.session.get('cart'), {})

    def test_checkout_rejects_another_users_address(self):
        Address.objects.create(
            user=self.user,
            full_name='Jane Doe',
            phone='9800000000',
            line1='123 Main Street',
            line2='',
            city='Mumbai',
            state='Maharashtra',
            postal_code='400001',
            country='India',
        )
        other_user = get_user_model().objects.create_user(username='other-user', password='test-pass-123')
        other_address = Address.objects.create(
            user=other_user,
            full_name='Other User',
            phone='9800000001',
            line1='456 Other Street',
            line2='',
            city='Pune',
            state='Maharashtra',
            postal_code='411001',
            country='India',
        )
        session = self.client.session
        session['cart'] = {str(self.product.id): {'price': str(self.product.price), 'qty': 1}}
        session.save()

        response = self.client.post(reverse('checkout'), {'selected_address_id': other_address.id})

        self.assertRedirects(response, reverse('checkout'))
        self.assertFalse(Order.objects.filter(user=self.user).exists())
