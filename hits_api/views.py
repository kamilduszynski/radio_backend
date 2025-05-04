# Third-party Imports
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Hit
from .serializers import HitSerializer


class HitListView(generics.ListAPIView):
    queryset = Hit.objects.order_by("-created_at")[:20]
    serializer_class = HitSerializer


class HitDetailView(APIView):
    def get(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        serializer = HitSerializer(hit)
        return Response(serializer.data)

    def put(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        data = request.data.copy()
        if "title" in data:
            data["title_url"] = slugify(data["title"])
        serializer = HitSerializer(hit, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        hit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HitCreateView(generics.CreateAPIView):
    serializer_class = HitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.title_url = slugify(instance.title)
            instance.save()
            return Response(
                HitSerializer(instance).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
