from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import SignUpView, ProfileEditView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
	path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
