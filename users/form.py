from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"example@gmail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(attrs={"placeholder": "Enter Username"}),
            'email': forms.EmailInput(attrs={"placeholder": "example@gmail.com"}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50'})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"}))
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        widget_attrs = {
            'class': 'w-full rounded-lg border border-slate-200 px-3 py-2 text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
        }
        for field in self.fields.values():
            field.widget.attrs.update(widget_attrs)
            


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        exclude = ['password1','password2']

        widgets = {
            'username':forms.TextInput(attrs={"placeholder":"Enter Username"}),
            'email':forms.TextInput(attrs={"placeholder":"example@gmail.com"})
    }