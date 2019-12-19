from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from . import serializers
from .models import Dog
from .serializers import DogSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogLikedRetrieveView(RetrieveAPIView):
    """API endpoint handling GET requests for dogs liked by user
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    # permission_classes = [] <- is authenticated

    def get_queryset(self):
        liked_dogs = self.queryset.filter(
            userdog__status='l',
            userdog__user_id=self.request.user.id,
        ).order_by('pk')
        return liked_dogs
    
    def get_object(self):
        liked_dogs = self.get_queryset()
        next_dogs = liked_dogs.filter(
            id__gt=self.kwargs.get('pk')
        )
        if next_dogs:
            return next_dogs.first()
        return liked_dogs.first()
        

class DogUndecidedRetrieveView(RetrieveAPIView):
    """API endpoint handling GET requests for dogs liked by user
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    # permission_classes = [] <- is authenticated

    def get_queryset(self):
        undecided_dogs = self.queryset.exclude(
            userdog__user_id=self.request.user.id
        ).order_by('pk')
        return undecided_dogs
    
    def get_object(self):
        undecided_dogs = self.get_queryset()
        next_dogs = undecided_dogs.filter(
            id__gt=self.kwargs.get('pk')
        )
        if next_dogs:
            return next_dogs.first()
        return undecided_dogs.first()






