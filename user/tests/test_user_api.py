from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import Group

CREATE_USER_URL = reverse('user:user-list')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
COUNT_USERS_URL = reverse('user:count')


def sample_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserTest(TestCase):
    """ Probar api usuarios de forma publica """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ crear usuario por el api """
        payload = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'password',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_create_duplicated(self):
        """ crear usuarios duplicados """
        payload = {
            'email': 'test@test.com',
            'password': 'password'
        }
        sample_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_shot_password(self):
        """ create user with short password """
        payload = {
            'email': 'test@test.com',
            'password': 'pw'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        # validar que me envie error 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # validar que no haya creado el usuario
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_get_token(self):
        """ obtain token by api """
        payload = {
            'email': 'test@test.com',
            'password': 'password',
        }
        sample_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_token_wrong_password(self):
        """ obtener token contrase~na incorrecta """
        sample_user(email='test@test.com', password='test123')
        response = self.client.post(TOKEN_URL, {'email': 'test@test.com', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_get_token_no_user(self):
        """ obtener token credenciales incorrectas """
        response = self.client.post(TOKEN_URL, {'email': 'test@test.com', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_get_token_missing_field(self):
        """ obtener token  """
        response = self.client.post(TOKEN_URL, {'email': 'test@test.com', 'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_retrieve_no_authorization(self):
        """ obtenet perfil sin estar logeado """
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cout_users(self):
        """ counter of users """
        sample_user(email='test@gmail.com', password='lol123lol')
        response = self.client.get(COUNT_USERS_URL)
        count = get_user_model().objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count)


class PrivateUserApi(TestCase):
    """ Clase para probar funcionalidades privadas api modelo user """

    def setUp(self):
        ''' configuracion inicial para las pruebas '''
        self.user = sample_user(email='test@test.com', password='test123', name='Test name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        ''' probar el obtener la informacion del perfil '''

        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': 'test@test.com',
            'name': 'Test name'
        })

    def test_delete_profile_success(self):
        ''' test delete me user '''

        response = self.client.delete(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_me_not_allowed(self):
        ''' probar POST no permitido '''
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        ''' Probar el usuario esta siendo actualizado si esta autenticado '''
        payload = {'name': 'New Name', 'password': 'newpassword'}
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))