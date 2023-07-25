from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from location.serializer import StateSerializer
from django.contrib.auth import get_user_model
from core import models
from location.tests.utils import sample_country

STATE_URL = reverse('location:state-list')


def retrieve_state_url(id_state):
    return reverse('location:state-detail', args=[id_state])


class PublicStateApiTest(TestCase):
    """
    class test state model
     """

    def setUp(self):
        self.client = APIClient()

    def test_state_list(self):
        """
        test get list states
        """
        country = sample_country()
        models.State.objects.create(name='state one', code=1, country=country)
        models.State.objects.create(name='state two', code=2, country=country)

        states = models.State.objects.all()
        serializer = StateSerializer(states, many=True)

        response = self.client.get(STATE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_retrieve_state(self):
        """
        test get state by id
        """
        country = sample_country()
        state = models.State.objects.create(name='state', code=1, country=country)
        url = retrieve_state_url(state.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)

    def test_update_unauthorized(self):
        """
        test retrieve state if not authenticated
        """
        country = sample_country()
        state = models.State.objects.create(name='state', code=1, country=country)
        url = retrieve_state_url(state.id)
        payload = {
            'name': 'state test',
            'code': 2
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStateApiTest(TestCase):
    """
    test create state if is admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(email='test@test.com', name='test', password='test123')
        self.client.force_authenticate(user=self.admin)

    def test_create_state(self):
        """
        test create state user admin
        """
        country = sample_country()
        payload = {
            'name': 'state',
            'code': 1,
            'country': country.id
        }
        response = self.client.post(STATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], payload['name'])

    def test_update_authorized(self):
        """
        test retrieve state if authenticated is admin
        """
        country = sample_country()
        state = models.State.objects.create(name='state', code=1, country=country)
        url = retrieve_state_url(state.id)
        payload = {
            'name': 'state test',
            'code': 2,
            'country': country.id
        }
        response = self.client.put(url, payload)
        state = models.State.objects.get(**response.data)
        serializer = StateSerializer(state, many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_authorized(self):
        """
        test delete state if authenticated is admin
        """
        country = sample_country()
        state = models.State.objects.create(name='state', code=1, country=country)
        url = retrieve_state_url(state.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        exists_state = models.State.objects.filter(pk=state.id).exists()
        self.assertFalse(exists_state)


class PrivateStateApiTestNotAmin(TestCase):
    """
    validate private url if not admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@user.com', name='user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_delete_forbidden(self):
        """
        test retrieve state if not authenticated
        """
        country = sample_country()
        state = models.State.objects.create(name='state', code=1, country=country)
        url = retrieve_state_url(state.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
