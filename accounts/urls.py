from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('<str:username>/', views.profile_detail_or_update),
    path('<str:username>/follow/', views.follow),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
