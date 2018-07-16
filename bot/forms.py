from django.contrib.auth import authenticate, get_user_model
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from bot.models import *
from django.contrib import admin
from django.core.validators import validate_email
from django.db.models import Q
from django.conf import settings

# from user.models import Profile


# class ProfileCreationForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ("fullname", 'email')


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    # fullname = forms.CharField(label=_("Full name"))
    # emailid = forms.CharField(label=_("Email ID"))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError("credentials not match")
            else:
                return self.cleaned_data


class EmailSubscribeForm(forms.ModelForm):

    class Meta:
        model = EmailSubscribe
        fields = ('email',)

    def save(self, commit=True):
        subscribe = super(EmailSubscribeForm, self).save(commit=True)
        subscribe.save()
        print('form')
        if commit:
            subscribe.save()
        return subscribe


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')

    def save(self, commit=True):
        contact = super(ContactForm, self).save(commit=True)
        contact.save()
        # print('form')
        if commit:
            contact.save()
        return contact


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Exchange
        fields = ('key', 'secret')
