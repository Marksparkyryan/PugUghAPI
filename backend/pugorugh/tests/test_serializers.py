from django.contrib.auth.models import User
from django.test import TestCase

from pugorugh.models import Dog, UserDog
from pugorugh.serializers import DogSerializer


class DogSerializerTestCases(TestCase):
    def setUp(self):
        # Userpref instance should be automatically created once user is created
        User.objects.create(
            username="sparky",
            email="sparky@email.com",
            password="password123"
        )
        Dog.objects.create(
            name="Dog1",
            image_filename="dog1.jpg",
            breed="pug",
            age=10,
            gender="f",
            size="s",
        )
        Dog.objects.create(
            name="Dog2",
            image_filename="dog2.jpg",
            breed="husky",
            age=20,
            gender="m",
            size="l",
        )
        Dog.objects.create(
            name="Dog3",
            image_filename="dog1.gif",
            breed="lab",
            age=15,
            gender="f",
            size="m",
        )
        UserDog.objects.create(
            user=User.objects.get(username="sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        UserDog.objects.create(
            user=User.objects.get(username="sparky"),
            dog=Dog.objects.get(name="Dog2"),
            status="d"
        )

    def test_fields(self):
        dog = Dog.objects.get(id=1)
        data = DogSerializer(dog).data
        self.assertEqual(
            set(data.keys()),
            set(['id',
                 'name',
                 'image_filename',
                 'breed',
                 'age',
                 'gender',
                 'size',
                 'birthday',
                 'likes',
                 'joined', ]
                ))
