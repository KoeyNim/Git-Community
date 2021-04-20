from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from django.utils.translation import ugettext_lazy as _

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")

class SocialUserForm(forms.Form):
    first_name = forms.CharField(label=_('First name'),
                                 max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'placeholder':
                                                _('First name'), }))
    last_name = forms.CharField(label=_('Last name'),
                                max_length=30,
                                widget=forms.TextInput(
                                    attrs={'placeholder':
                                               _('Last name'), }))
    phone = forms.CharField(label=_('Phone number'),
                            max_length=30,
                            widget=forms.TextInput(
                                attrs={'placeholder':
                                           _('Phone number'), }))

    def signup(self, request, name):
        name.first_name = self.cleaned_data['first_name']
        name.last_name = self.cleaned_data['last_name']
        name.save()

        profile = User
        profile.name = name
        profile.phone = self.cleaned_data['phone']
        profile.save()
