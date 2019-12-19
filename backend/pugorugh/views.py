from django.contrib.auth import get_user_model
from django.shortcuts import Http404

from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from . import serializers
from .models import Dog
from .serializers import DogSerializer


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
    permission_classes = [permissions.IsAuthenticated]

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
        raise Http404()
