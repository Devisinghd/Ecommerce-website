from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class EmailVerificationCode(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification_code')
	code_hash = models.CharField(max_length=128)
	expires_at = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	def is_expired(self):
		return timezone.now() >= self.expires_at

	@classmethod
	def expiry_time(cls, minutes=10):
		return timezone.now() + timedelta(minutes=minutes)
