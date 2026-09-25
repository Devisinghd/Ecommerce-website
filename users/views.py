import logging
import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render
from .form import CreateUserForm, EmailVerificationForm, UserUpdateForm
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db import transaction
from .models import EmailVerificationCode
from .form import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            if not settings.EMAIL_VERIFICATION:
                user.is_active = True
                user.save()
                messages.success(request, 'Account created successfully. You may now log in.')
                return redirect('login')

            user.is_active = False
            user.save()

            try:
                verification_code = f'{secrets.randbelow(1_000_000):06d}'
                with transaction.atomic():
                    EmailVerificationCode.objects.update_or_create(
                        user=user,
                        defaults={
                            'code_hash': make_password(verification_code),
                            'expires_at': EmailVerificationCode.expiry_time(settings.EMAIL_OTP_EXPIRY_MINUTES),
                        },
                    )

                html_message = render_to_string('users/email-verification.html', {
                    'user': user,
                    'verification_code': verification_code,
                    'expiry_minutes': settings.EMAIL_OTP_EXPIRY_MINUTES,
                })
                plain_message = (
                    f'Hi {user.username}, your ShopFusion email verification code is '
                    f'{verification_code}. It expires in {settings.EMAIL_OTP_EXPIRY_MINUTES} minutes.'
                )
                user.email_user(
                    subject='Your ShopFusion email verification code',
                    message=plain_message,
                    html_message=html_message,
                    fail_silently=False,
                )

                request.session['pending_verification_user_id'] = user.pk
                messages.success(request, 'Account created successfully. Check your email to activate the account.')
                return redirect('email-verification-sent')
            except Exception:
                logger.exception('Failed to render/send verification email for user %s.', user.username)
                messages.error(request, 'We could not send the verification code. Please try again later.')
                return redirect('register')

    return render(request,'users/register.html', {'form': form})


def email_verification(request):
    user_id = request.session.get('pending_verification_user_id')
    user = User.objects.filter(pk=user_id, is_active=False).first()
    if user is None:
        return redirect('email-verification-failed')

    form = EmailVerificationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        verification = EmailVerificationCode.objects.filter(user=user).first()
        if verification and not verification.is_expired() and check_password(form.cleaned_data['code'], verification.code_hash):
            user.is_active = True
            user.save(update_fields=['is_active'])
            verification.delete()
            request.session.pop('pending_verification_user_id', None)
            return redirect('email-verification-success')
        form.add_error('code', 'That code is invalid or expired.')

    return render(request, 'users/email-verification-sent.html', {
        'form': form,
        'expiry_minutes': settings.EMAIL_OTP_EXPIRY_MINUTES,
    })

def email_verification_sent(request):
    return email_verification(request)

def email_verification_success(request):
    return render(request,'users/email-verification-success.html')

def email_verification_failed(request):
    return render(request,'users/email-verification-failed.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request,'users/logout-confirmation.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('index')
    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request,'users/profile.html',{'user_form':user_form})

@login_required
def profile_view(request,id):
    user = get_object_or_404(User, pk=id)
    return render(request,'users/profile-view.html',{'user':user})
