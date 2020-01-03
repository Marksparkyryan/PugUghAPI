from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref
from pugorugh.serializers import DogSerializer


class DogTestCases(TestCase):
    def setUp(self):
        #Userpref instance should be automatically created once user is created
        User.objects.create(
            username="Sparky",
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
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        UserDog.objects.create(
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog2"),
            status="d"
        )

    def test_model_objects_created(self):
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserPref.objects.all().count(), 1)
        self.assertEqual(Dog.objects.all().count(), 3)
        self.assertEqual(UserDog.objects.all().count(), 2)
    
    def test_age_letter_auto_creation(self):
        dog = Dog.objects.get(id=1)
        self.assertRegex(dog.age_letter, r'(s|a|y|b)')
    
    def test_dog_str_method(self):
        dog = Dog.objects.get(id=2)
        self.assertEqual(str(dog), "Dog2")
    
    def test_dog_likes_property(self):
        dog = Dog.objects.get(id=1)
        self.assertRegex(str(dog.likes), r'\d+')
    
    def test_dog_age_letter_update(self):
        dog = Dog.objects.get(id=1)
        self.assertEqual(dog.age_letter, "y")
        dog.age = 20
        dog.save()
        self.assertEqual(dog.age_letter, "a")
        dog.age = 85
        dog.save()
        self.assertEqual(dog.age_letter, "s")
        dog.age = 1
        dog.save()
        self.assertEqual(dog.age_letter, "b")
        dog.age = -1
        dog.save()
        self.assertEqual(dog.age_letter, "b")


class UserDogTestCases(TestCase):
    def setUp(self):
        #Userpref instance should be automatically created once user is created
        User.objects.create(
            username="Sparky",
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
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        UserDog.objects.create(
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog2"),
            status="d"
        )
    
    def test_userdog_str_method(self):
        userdog = UserDog.objects.get(id=1)
        self.assertAlmostEqual(str(userdog), "Sparky liked Dog1")

    def test_uniqueness_of_userdog(self):
        duplicate_userdog = UserDog(
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        with self.assertRaises(IntegrityError):
            duplicate_userdog.save()


class UserPrefTestCases(TestCase):
    def setUp(self):
        #Userpref instance should be automatically created once user is created
        User.objects.create(
            username="Sparky",
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
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        UserDog.objects.create(
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog2"),
            status="d"
        )
    
    def test_userpref_str_method(self):
        prefs = UserPref.objects.get(id=1)
        self.assertAlmostEqual(str(prefs), "Sparky's preferences")


class DogSerializerTestCases(TestCase):
    def setUp(self):
        #Userpref instance should be automatically created once user is created
        User.objects.create(
            username="Sparky",
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
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        UserDog.objects.create(
            user=User.objects.get(username="Sparky"),
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


class APIViewTestCases(TestCase):
    def setUp(self):
        #Userpref instance should be automatically created once user is created
        User.objects.create(
            username="Sparky",
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
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog1"),
            status="l"
        )
        UserDog.objects.create(
            user=User.objects.get(username="Sparky"),
            dog=Dog.objects.get(name="Dog2"),
            status="d"
        )

    #test views here

    


       

        
