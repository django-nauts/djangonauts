from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import ProfileEditForm, SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('profile_edit')  # Redirect to the same page after successful edit

    def get_object(self):
        return self.request.user.profile  # Get the profile of the logged-in user
