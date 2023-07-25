from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core import models
from location.tests.utils import sample_state, sample_city
from location.serializer import CitySerializer

CITY_URL = reverse('location:city-list')


def retrieve_city_url(id_city):
    return reverse('location:city-detail', args=[id_city])


class PublicCityApiTest(TestCase):
    """
    class test city model
     """

    def setUp(self):
        self.client = APIClient()

    def test_city_list(self):
        """
        test get list cities
        """
        state = sample_state()
        models.City.objects.create(name='city one', code=1, state=state)
        models.City.objects.create(name='city two', code=2, state=state)

        cities = models.City.objects.all()
        serializer = CitySerializer(cities, many=True)

        response = self.client.get(CITY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_retrieve_city(self):
        """
        test get city by id
        """
        city = sample_city()
        url = retrieve_city_url(city.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)

    def test_update_unauthorized(self):
        """
        test retrieve city if not authenticated
        """
        state = sample_state()
        city = sample_city(name='city test', code=2)
        url = retrieve_city_url(city.id)
        payload = {
            'name': 'city edit',
            'code': 3,
            'state': state.id
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCityApiTest(TestCase):
    """
    test create city if is admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(email='test@test.com', name='test', password='test123')
        self.client.force_authenticate(user=self.admin)

    def test_create_city(self):
        """
        test create city user admin
        """
        state = sample_state()
        payload = {
            'name': 'city',
            'code': 1,
            'state': state.id
        }
        response = self.client.post(CITY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], payload['name'])

    def test_update_authorized(self):
        """
        test retrieve city if authenticated is admin
        """
        state = sample_state()
        city = sample_city(name='city test', code=2)
        url = retrieve_city_url(city.id)
        payload = {
            'name': 'city test',
            'code': 2,
            'state': state.id
        }
        response = self.client.put(url, payload)
        city = models.City.objects.get(**response.data)
        serializer = CitySerializer(city, many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_authorized(self):
        """
        test delete city if authenticated is admin
        """
        city = sample_city()
        url = retrieve_city_url(city.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        exists_city = models.City.objects.filter(pk=city.id).exists()
        self.assertFalse(exists_city)


class PrivateCityApiTestNotAmin(TestCase):
    """
    validate private url if not admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@user.com', name='user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_delete_forbidden(self):
        """
        test retrieve city if not authenticated
        """
        city = sample_city()
        url = retrieve_city_url(city.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
