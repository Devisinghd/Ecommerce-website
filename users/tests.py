from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core import mail
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import EmailVerificationCode


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


@override_settings(EMAIL_VERIFICATION=True, EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class EmailOtpVerificationTests(TestCase):
    def test_registration_sends_otp_instead_of_link(self):
        response = self.client.post(reverse('register'), {
            'username': 'otpuser',
            'email': 'otpuser@example.com',
            'password1': 'strong-pass-123',
            'password2': 'strong-pass-123',
        })

        self.assertRedirects(response, reverse('email-verification-sent'))
        self.assertFalse(get_user_model().objects.get(username='otpuser').is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertRegex(mail.outbox[0].body, r'\b\d{6}\b')
        self.assertNotIn('email-verification/', mail.outbox[0].body)

    def test_valid_otp_activates_user_once(self):
        user = get_user_model().objects.create_user(
            username='pendingotp',
            email='pendingotp@example.com',
            password='strong-pass-123',
            is_active=False,
        )
        code = '123456'
        EmailVerificationCode.objects.create(
            user=user,
            code_hash=make_password(code),
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        session = self.client.session
        session['pending_verification_user_id'] = user.pk
        session.save()

        response = self.client.post(reverse('email-verification'), {'code': code})

        self.assertRedirects(response, reverse('email-verification-success'))
        self.assertTrue(get_user_model().objects.get(pk=user.pk).is_active)
        self.assertFalse(EmailVerificationCode.objects.filter(user=user).exists())

    def test_expired_otp_does_not_activate_user(self):
        user = get_user_model().objects.create_user(
            username='expiredotp',
            email='expiredotp@example.com',
            password='strong-pass-123',
            is_active=False,
        )
        EmailVerificationCode.objects.create(
            user=user,
            code_hash=make_password('123456'),
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        session = self.client.session
        session['pending_verification_user_id'] = user.pk
        session.save()

        response = self.client.post(reverse('email-verification'), {'code': '123456'})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.get(pk=user.pk).is_active)
        self.assertContains(response, 'invalid or expired')
