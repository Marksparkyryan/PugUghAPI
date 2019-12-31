from django.contrib.auth import get_user_model
from django.shortcuts import Http404, get_object_or_404
from django.core.urlresolvers import reverse

from rest_framework import permissions, status
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, RetrieveUpdateAPIView,
                                     ListCreateAPIView, DestroyAPIView)
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers
from .models import Dog, UserDog, UserPref
from .serializers import DogSerializer, UserDogSerializer, UserPrefSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogListCreateView(ListCreateAPIView):
    """API endpoint handling the GET and POST requests for dogs
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticated]


class DogDeleteView(DestroyAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticated]


class DogRetrieveView(RetrieveAPIView):
    """API endpoint handling GET requests for dogs liked, disliked, or
    undecided by user.
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        feeling = self.kwargs.get('feeling')[0]
        if feeling in ('l', 'd'):
            feeling_dogs = self.queryset.filter(
                userdog__status=feeling,
                userdog__user_id=self.request.user.id,
            ).order_by('pk')
        elif feeling == 'u':
            feeling_dogs = self.queryset.filter(
                age_letter__in=self.request.user.prefs.age,
                gender__in=self.request.user.prefs.gender,
                size__in=self.request.user.prefs.size
            ).exclude(
                userdog__user_id=self.request.user.id
            ).order_by('pk')
        return feeling_dogs

    def get_object(self):
        feeling_dogs = self.get_queryset()
        print("feeling_dogs queryset ", feeling_dogs)
        next_dogs = feeling_dogs.filter(
            id__gt=self.kwargs.get('pk')
        )
        print("next_dogs ", next_dogs)
        if next_dogs.exists():
            return next_dogs.first()
        if feeling_dogs.exists():
            return feeling_dogs.first()
        raise Http404()


class UserDogStatusUpdateView(UpdateAPIView):
    """API endpoint handling GET requests for dogs liked, disliked, or
    undecided by user
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        feeling = self.kwargs.get('feeling')[0]
        if feeling in ('l', 'd'):
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
                    'status': feeling
                })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif feeling == 'u':
            relationship = UserDog.objects.filter(
                user=self.request.user.id,
                dog=self.get_object().id
            )
            if relationship.exists():
                relationship.delete()
            dog = self.get_object()
            serializer = DogSerializer(instance=dog)
            return Response(serializer.data)


class UserPrefUpdateView(RetrieveUpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        userpref = self.get_queryset().filter(
            user=self.request.user
        ).first()
        return userpref
