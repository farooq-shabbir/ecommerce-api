from django.urls import path
from .views import health, upload_photo, list_photos

urlpatterns = [
    path("health/", health, name="health"),
    path("photos/", list_photos, name="photos-list"),
    path("photos/upload/", upload_photo, name="photos-upload"),
]
