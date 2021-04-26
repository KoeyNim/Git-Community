from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SocialUser

from django.utils.translation import ugettext_lazy as _

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    name = forms.CharField(label="이름")
    phone = forms.CharField(label="휴대폰번호")

    class Meta:
        model = User
        fields = ("username", "email", "name", "phone")

class SocialUserForm(forms.Form):

    name = forms.CharField(label=_('name'),
                            max_length=30,
                            widget=forms.TextInput(
                                attrs={'placeholder':
                                           _('name'), }))

    phone = forms.CharField(label=_('Phone number'),
                            max_length=30,
                            widget=forms.TextInput(
                                attrs={'placeholder':
                                           _('Phone number'), }))

    def signup(self, request, user):

        profile = SocialUser()
        profile.user = user
        profile.name = self.cleaned_data['name']
        profile.phone = self.cleaned_data['phone']
        profile.save()
