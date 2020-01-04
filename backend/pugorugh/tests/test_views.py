from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from pugorugh.models import Dog, UserDog, UserPref
from pugorugh.serializers import DogSerializer, UserPrefSerializer


class APIViewTestCases(TestCase):
    def setUp(self):
        # Userpref instance should be automatically created once user is created
        user = User.objects.create(
            username="sparky",
            email="sparky@email.com",
        )
        user.set_password('password123')
        user.save()

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

    user = User.objects.get(username='sparky')
    token = Token.objects.get(user=user)
    apiclient = APIClient()
    apiclient.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_user_register_view(self):
        # clear token from header before registering new user
        self.apiclient.credentials()
        response = self.apiclient.post(
            '/api/user/',
            {'username': 'Shay', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_list_doglistcreateview(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/',
            format='json'
        )
        expected = []
        for dog in Dog.objects.all():
            expected.append(DogSerializer(dog).data)
        self.assertJSONEqual(response.content, expected)

    def test_create_doglistcreateview(self):
        self.apiclient.force_authenticate(user=self.user)
        data = {
            "name": "alpha",
            "image_filename": "alpha.jpg",
            "breed": "husky",
            "age": "100",
            "gender": "m",
            "size": "l"
        }
        response = self.apiclient.post(
            '/api/dog/',
            data,
            format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_list_doglistcreateview_without_credentials(self):
        self.apiclient.force_authenticate(user=None)
        response = self.apiclient.get(
            '/api/dog/',
            format='json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"detail": "Authentication credentials were not provided."})

    def test_create_doglistcreateview_missing_field(self):
        self.apiclient.force_authenticate(user=self.user)
        data = {
            "name": "alpha",
            "breed": "husky",
            "age": "100",
            "gender": "m",
            "size": "l"
        }
        response = self.apiclient.post(
            '/api/dog/',
            data,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"image_filename": ["This field is required."]}
        )

    def test_dogdeleteview(self):
        self.apiclient.force_authenticate(user=self.user)
        self.assertEqual(Dog.objects.all().count(), 3)
        response = self.apiclient.delete(
            '/api/dog/3/',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Dog.objects.all().count(), 2)

    def test_dogdeleteview_bad_key(self):
        self.apiclient.force_authenticate(user=self.user)
        self.assertEqual(Dog.objects.all().count(), 3)
        response = self.apiclient.delete(
            '/api/dog/99/',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Dog.objects.all().count(), 3)
        self.assertJSONEqual(response.content, {"detail": "Not found."})

    def test_dogretrieveview_next_liked(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/-1/liked/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=1))
        self.assertJSONEqual(response.content, expected.data)
        response = self.apiclient.get(
            '/api/dog/1/liked/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=1))
        self.assertJSONEqual(response.content, expected.data)

    def test_dogretrieveview_next_liked_bad_key(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/99/liked/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=1))
        self.assertJSONEqual(response.content, expected.data)

    def test_dogretrieveview_next_disliked(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/-1/disliked/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=2))
        self.assertJSONEqual(response.content, expected.data)
        response = self.apiclient.get(
            '/api/dog/1/disliked/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=2))
        self.assertJSONEqual(response.content, expected.data)

    def test_dogretrieveview_next_disliked_bad_key(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/99/disliked/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=2))
        self.assertJSONEqual(response.content, expected.data)

    def test_dogretrieveview_next_undecided(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/-1/undecided/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=3))
        self.assertJSONEqual(response.content, expected.data)
        response = self.apiclient.get(
            '/api/dog/1/undecided/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=3))
        self.assertJSONEqual(response.content, expected.data)

    def test_dogretrieveview_next_undecided_bad_key(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.get(
            '/api/dog/99/undecided/next/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        expected = DogSerializer(Dog.objects.get(id=3))
        self.assertJSONEqual(response.content, expected.data)

    def test_userdogstatusupdateview_liked(self):
        self.apiclient.force_authenticate(user=self.user)
        queryset = UserDog.objects.filter(
            user=self.user,
            status='l'
        )
        self.assertEqual(queryset.count(), 1)
        response = self.apiclient.put(
            '/api/dog/3/liked/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        queryset = UserDog.objects.filter(
            user=self.user,
            status='l'
        )
        self.assertEqual(queryset.count(), 2)

    def test_userdogstatusupdateview_disliked(self):
        self.apiclient.force_authenticate(user=self.user)
        queryset = UserDog.objects.filter(
            user=self.user,
            status='d'
        )
        self.assertEqual(queryset.count(), 1)
        response = self.apiclient.put(
            '/api/dog/3/disliked/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        queryset = UserDog.objects.filter(
            user=self.user,
            status='d'
        )
        self.assertEqual(queryset.count(), 2)

    def test_userdogstatusupdateview_undecided(self):
        self.apiclient.force_authenticate(user=self.user)
        queryset = UserDog.objects.filter(
            user=self.user,
            status='u'
        )
        self.assertEqual(queryset.count(), 0)
        response = self.apiclient.put(
            '/api/dog/3/undecided/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        u_queryset = UserDog.objects.filter(
            user=self.user,
            status='u'
        )
        all_queryset = Dog.objects.all().exclude(
            userdog__user_id=self.user
        )
        self.assertEqual(u_queryset.count(), 0)
        self.assertEqual(all_queryset.count(), 1)

    def test_userprefupdateview(self):
        self.apiclient.force_authenticate(user=self.user)
        response = self.apiclient.put(
            '/api/user/preferences/',
            data={"age": "b", "gender": "f", "size": "s"},
            format='json'
        )
        expected = UserPrefSerializer(UserPref.objects.get(user=self.user))
        self.assertJSONEqual(
            response.content,
            expected.data
        )
