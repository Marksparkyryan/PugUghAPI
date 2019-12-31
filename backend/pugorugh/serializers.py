from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Dog, UserPref, UserDog


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    """Serialzer that encodes and decodes each field of the Dog
    model
    """
    class Meta:
        model = Dog
        fields = [
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
            'birthday',
            'likes'
        ]


class UserDogSerializer(serializers.ModelSerializer):
    """Serailizer that encodes and decodes each field of the UserDog
    model
    """
    class Meta:
        model = UserDog
        fields = [
            'user',
            'dog',
            'status',
        ]


class UserPrefSerializer(serializers.ModelSerializer):
    """Serializer that encodes and decodes each field of the UserPref
    model
    """
    class Meta:
        model = UserPref
        fields = [
            'age',
            'gender',
            'size',
        ]
