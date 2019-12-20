from django.contrib.auth import get_user_model
from django.shortcuts import Http404, get_object_or_404

from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response

from . import serializers
from .models import Dog, UserDog
from .serializers import DogSerializer, UserDogSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogRetrieveView(RetrieveAPIView):
    """API endpoint handling GET requests for dogs liked, disliked, or
    undecided by user
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        status = self.kwargs.get('status')[0]
        if status in ('l', 'd'):
            status_dogs = self.queryset.filter(
                userdog__status=status,
                userdog__user_id=self.request.user.id,
            ).order_by('pk')
        elif status == 'u':
            status_dogs = self.queryset.exclude(
                userdog__user_id=self.request.user.id
            ).order_by('pk')
        return status_dogs

    def get_object(self):
        status_dogs = self.get_queryset()
        next_dogs = status_dogs.filter(
            id__gt=self.kwargs.get('pk')
        )
        if next_dogs.exists():
            return next_dogs.first()
        if status_dogs.exists():
            return status_dogs.first()
        raise Http404()


class DogLikedDislikedUpdateView(UpdateAPIView):
    """API endpoint handling GET requests for dogs liked, disliked, or
    undecided by user
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        status = self.kwargs.get('status')[0]
        existing, created = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=self.get_object(),
        )
        instance = existing or created
        serializer = UserDogSerializer(
            instance=instance,
            data={
                'user': self.request.user.id,
                'dog': self.get_object().id,
                'status': status
            })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
