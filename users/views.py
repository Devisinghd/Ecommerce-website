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
# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            # email verification logic
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
            # send HTML email (html_message) with a simple plain-text fallback
            user.email_user(subject=subject, message=plain_message, html_message=html_message)
            return redirect('email-verification-sent')
            
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
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request,'users/logout-confirmation.html')


def profile(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('index')

    user_form = UserUpdateForm(instance=request.user)

    return render(request,'users/profile.html',{'user_form':user_form})

def profile_view(request):
    return render(request,'users/profile-view.html')
