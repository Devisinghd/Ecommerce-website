from django.shortcuts import redirect, render
from .form import CreateUserForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_str 
from .token import account_activation_token
# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            #email verification logic
            subject = 'Verify your email to activate account'
            message = render_to_string('users/email-verification.html',{
                'user':user,
                'domian': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            return redirect('email-verification-sent')
            
            return redirect('index')
    return render(request,'users/register.html', {'form': form})


def email_verification(request):
    pass

def email_verification_sent(request):
    return render(request,'users/email-verification-sent.html')

def email_verification_success(request):
    pass

def email_verification_failed(request):
    pass
