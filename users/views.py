import logging
import threading

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from .form import CreateUserForm , UserUpdateForm
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_str 
from .token import account_activation_token
from django.contrib.auth.models import User
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

            # email verification logic (render + send). Wrap entire block so
            # template rendering or SMTP errors don't bubble up as 500s.
            try:
                subject = 'Verify your email to activate account'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                verification_path = reverse('email-verification', kwargs={'uidb64': uid, 'token': token})
                absolute_url = request.build_absolute_uri(verification_path)
                html_message = render_to_string('users/email-verification.html', {
                    'user': user,
                    'verification_link': absolute_url,
                })
                plain_message = f"Hi {user.username}, please verify your email by visiting: {absolute_url}"

                def _send_verification_email(subject, plain_message, html_message, user):
                    try:
                        user.email_user(
                            subject=subject,
                            message=plain_message,
                            html_message=html_message,
                            fail_silently=True,
                        )
                    except Exception:
                        logger.exception('Background email send failed for user %s', user.username)

                try:
                    thread = threading.Thread(
                        target=_send_verification_email,
                        args=(subject, plain_message, html_message, user),
                        daemon=True,
                    )
                    thread.start()
                except Exception:
                    logger.exception('Failed to start background thread for sending email for user %s', user.username)

                messages.success(request, 'Account created successfully. Check your email to activate the account.')
                return redirect('email-verification-sent')
            except Exception:
                # Log the full exception for debugging and fall back to
                # activating the account so the user can proceed.
                logger.exception('Failed to render/send verification email for user %s.', user.username)
                user.is_active = True
                user.save()
                messages.warning(request, 'Account created, but the verification email could not be sent. You can log in now.')
                return redirect('login')

    return render(request,'users/register.html', {'form': form})


def email_verification(request, uidb64, token):
    try:
        unique_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=unique_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request,'users/email-verification-sent.html')

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
