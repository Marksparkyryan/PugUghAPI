from django.contrib.auth import get_user_model
from django.shortcuts import Http404

from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, RetrieveUpdateAPIView,
                                     ListCreateAPIView, DestroyAPIView)
from rest_framework.response import Response

from . import serializers
from .models import Dog, UserDog, UserPref
from .serializers import DogSerializer, UserDogSerializer, UserPrefSerializer


class UserRegisterView(CreateAPIView):
    """API endpoint handling the registration of new users
    """
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
    """API endpoint handling the deletion of single Dog instances
    """
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
        """Takes in kwargs from uri (l, d, or u) and filters/returns Dog
        queryset
        """
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
        next_dogs = feeling_dogs.filter(
            id__gt=self.kwargs.get('pk')
        )
        if next_dogs.exists():
            return next_dogs.first()
        if feeling_dogs.exists():
            return feeling_dogs.first()
        raise Http404()


class UserDogStatusUpdateView(UpdateAPIView):
    """API endpoint handling GET requests for dogs liked, disliked, or
    undecided by user. Note, relationships that are undecided are not
    created and stored on the UserDog table. We can assume all dogs that
    are not liked or disliked are undecided. We can exclude dogs that
    exist in the UserDog table to get a queryset of all undecided dogs.
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
    """API endpoint handling the update of User's preference of Dog
    """
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        userpref = self.get_queryset().filter(
            user=self.request.user
        ).first()
        return userpref
