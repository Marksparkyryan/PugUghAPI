from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """Model decribing a dog

    Attributes:
        name {string} -- name of the dog
        image_filename {string} -- filename of dog's image
        breed {string} -- breed of the dog
        age {integer} -- age of dog in months
        gender {string} -- one character [(m)ale, (f)emale, (u)nknown]
        representing gender of dog
        size {string} -- character(s) [(s)mall, (m)edium, (l)arge, (xl)
        extra large, (u)nknown] representing size of dog
    """
    GENDER = (
        ('m', 'male'),
        ('f', 'female'),
        ('u', 'unknown'),
    )

    SIZE = (
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large'),
        ('u', 'unknown')
    )

    name = models.CharField(max_length=48, unique=True)
    image_filename = models.CharField(max_length=256, unique=True)
    breed = models.CharField(default='unknown', max_length=48)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    size = models.CharField(default="unknown", max_length=2, choices=SIZE)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """Model representing the relationship (liked or disliked) between
    each user and each dog

    Attributes:
        user {ForeignKey} -- Many to one relationship to a user
        dog {ForeignKey} -- Many to one relationship to a dog
        status {string} -- one character [(l)iked, (d)isliked]
        representing how a user feels about a dog
    """
    FEELINGS = (
        ('l', 'liked'),
        ('d', 'disliked')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=FEELINGS)

    class Meta:
        unique_together = ['user', 'dog']


class UserPref(models.Model):
    """Model representing each user's preferences of dog

    Attributes:
        user {ForeignKey} -- owner (user) of these prefences
        age {string} -- character [(b)aby, (y)oung, (a)dult, (s)enior]
        representing preffered age of dog
        gender {string} -- character [(m)ale, (f)emale] representing
        preferred gender of dog
        size {string} -- character(s)
        [(s)mall, (m)edium, (l)arge, (xl) extra large] representing
        preferred size of dog
    """
    AGES = (
        ('b', 'baby'),
        ('y', 'young'),
        ('a', 'adult'),
        ('s', 'senior')
    )

    GENDERS = (
        ('m', 'male'),
        ('f', 'female')
    )

    SIZES = (
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
        ('xl', 'extra large')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=1, choices=AGES)
    gender = models.CharField(max_length=1, choices=GENDERS)
    size = models.CharField(max_length=2, choices=SIZES)
