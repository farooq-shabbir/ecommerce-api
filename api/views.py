from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.shortcuts import redirect
from .models import Photo


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


@api_view(["POST"])
def upload_photo(request):
    parser_classes = (MultiPartParser, FormParser)
    if "image" not in request.FILES:
        return Response({"detail": "image file is required"}, status=status.HTTP_400_BAD_REQUEST)
    photo = Photo.objects.create(image=request.FILES["image"])
    url = f"{settings.MEDIA_URL}{photo.image}"
    return Response({"id": photo.id, "url": url}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_photos(request):
    items = [{"id": p.id, "url": f"{settings.MEDIA_URL}{p.image}"} for p in Photo.objects.order_by("-id")]
    return Response(items)
