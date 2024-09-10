from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'profile_image')

def save(self, commit=True):
    user = super().save(commit)
    profile, created = Profile.objects.get_or_create(user=user)
    profile_image = self.cleaned_data.get('profile_image')
    if profile_image:
        profile.profile_image = profile_image
    else:
        profile.profile_image = 'default_profile.png'  # Set default image path
    if commit:
        profile.save()
    return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']
