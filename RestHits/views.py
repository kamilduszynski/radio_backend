from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Hit
from .serializers import HitSerializer


class HitViewSet(viewsets.ViewSet):
    def list(self, request):
        hits = Hit.objects.order_by("-created_at")[:20]
        serializer = HitSerializer(hits, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        hit = get_object_or_404(Hit, title_url=pk)
        serializer = HitSerializer(hit)
        return Response(serializer.data)

    def create(self, request):
        serializer = HitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        hit = get_object_or_404(Hit, title_url=pk)
        serializer = HitSerializer(hit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        hit = get_object_or_404(Hit, title_url=pk)
        hit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
