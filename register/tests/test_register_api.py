from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core import models
from location.tests.utils import sample_city
from register.serializer import CitizenListSerializer

REGISTER_URL = reverse('register:citizen-list')


def detail_url(id_citizen):
    return reverse('register:citizen-detail', args=[id_citizen])


def sample_register(user, city, **kwargs):
    payload = {
        'name': 'people',
        'last_name': 'test',
        'address': 'cll 30',
        'phone': '3213860504',
        'no_identification': '1234567890',
        'city': city
    }
    payload.update(kwargs)
    return models.Citizen.objects.create(user=user, **payload)


class PublicRegisterApiTest(TestCase):
    """ tests api by access public """

    def setUp(self):
        self.client = APIClient()

    def test_list_unauthorized(self):
        """ test get list people registered """
        response = self.client.get(REGISTER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRegisterApiTest(TestCase):
    """ tests api by access private """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@test.com', name='test', password='test1234')
        self.client.force_authenticate(user=self.user)

    def test_create_success(self):
        """ register people """
        city = sample_city(name='city 1')
        payload = {
            'name': 'people',
            'last_name': 'test',
            'address': 'cll 30',
            'phone': '3213860504',
            'no_identification': '1234567890',
            'city': city.id
        }
        response = self.client.post(REGISTER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertIn('name', response.data)

    def test_listed_by_user(self):
        """ test list peoples registered by user """
        city = sample_city('city 1', code=1)
        sample_register(user=self.user, city=city, name='test', last_name='one')

        user1 = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        sample_register(user=user1, city=city, name='test', last_name='two')

        response = self.client.get(REGISTER_URL)
        citizens = models.Citizen.objects.filter(user=self.user)
        serializer = CitizenListSerializer(citizens, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # def test_retrieve_citizen(self):
    #     """ test retrieve citizen by id """
    #     city = sample_city('city one', code=1)
    #     citizen = sample_register(user=self.user, city=city, name='person', last_name='one')
    #     serializer = CitizenListSerializer(citizen)
    #     url = detail_url(citizen.id)
    #     response = self.client.get(url)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_citizen_by_not_user(self):
        """ test retrieve citizen when citizen not belong to user """
        city = sample_city('city one', code=1)
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        citizen = sample_register(user=user, city=city, name='person', last_name='one')
        url = detail_url(citizen.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_citizen(self):
        """ test update citizen by id """
        city = sample_city('city one', code=1)
        citizen = sample_register(user=self.user, city=city, name='person', last_name='edit')
        payload = {
            'name': 'people',
            'last_name': 'edit',
            'address': 'cll 30',
            'phone': '3213860504',
            'no_identification': '1234567890',
            'city': city.id
        }
        url = detail_url(citizen.id)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], payload['last_name'])

    def test_update_citizen_by_not_user(self):
        """ test update citizen when citizen not belong to user """
        city = sample_city('city one', code=1)
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        citizen = sample_register(user=user, city=city, name='person', last_name='one')
        url = detail_url(citizen.id)
        payload = {
            'name': 'person',
            'last_name': 'edit'
        }
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_citizen(self):
        """ test delete citizen by id """
        city = sample_city('city one', code=1)
        citizen = sample_register(user=self.user, city=city, name='person', last_name='one')
        url = detail_url(citizen.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_citizen_by_not_user(self):
        """ test delete citizen when citizen not belong to user """
        city = sample_city('city one', code=1)
        user = get_user_model().objects.create_user(email='person@person.com', name='person 1', password='test123')
        citizen = sample_register(user=user, city=city, name='person', last_name='one')
        url = detail_url(citizen.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
