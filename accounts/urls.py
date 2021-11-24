from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', views.profile_create),
    path('<str:username>/', views.profile_detail_or_update),
    path('<str:username>/follow/', views.follow),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
