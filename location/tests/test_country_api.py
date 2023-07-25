from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from core import models
from location.serializer import CountrySerializer
from django.contrib.auth import get_user_model

COUNTRY_URL = reverse('location:country-list')


def retrieve_country_url(id_country):
    return reverse('location:country-detail', args=[id_country])


class PublicCountryApiTest(TestCase):
    """
    class test country model
     """

    def setUp(self):
        self.client = APIClient()

    def test_country_list(self):
        """
        test get list cities
        """
        models.Country.objects.create(name='country one', code=1)
        models.Country.objects.create(name='country two', code=2)

        countries = models.Country.objects.all()
        serializer = CountrySerializer(countries, many=True)

        response = self.client.get(COUNTRY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_retrieve_country(self):
        """
        test get country by id
        """
        country = models.Country.objects.create(name='country', code=1)
        url = retrieve_country_url(country.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)

    def test_update_unauthorized(self):
        """
        test retrieve country if not authenticated
        """
        country = models.Country.objects.create(name='country', code=1)
        url = retrieve_country_url(country.id)
        payload = {
            'name': 'country test',
            'code': 2
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCountryApiTest(TestCase):
    """
    test create country if is admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(email='test@test.com', name='test', password='test123')
        self.client.force_authenticate(user=self.admin)

    def test_create_country(self):
        """
        test create country user admin
        """
        payload = {
            'name': 'country',
            'code': 1
        }
        response = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], payload['name'])

    def test_update_authorized(self):
        """
        test retrieve country if authenticated is admin
        """
        country = models.Country.objects.create(name='country', code=1)
        url = retrieve_country_url(country.id)
        payload = {
            'name': 'country test',
            'code': 2
        }
        response = self.client.put(url, payload)
        country = models.Country.objects.get(**response.data)
        serializer = CountrySerializer(country, many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_authorized(self):
        """
        test delete country if authenticated is admin
        """
        country = models.Country.objects.create(name='country', code=1)
        url = retrieve_country_url(country.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        exists_country = models.Country.objects.filter(pk=country.id).exists()
        self.assertFalse(exists_country)


class PrivateCountryApiTestNotAmin(TestCase):
    """
    validate private url if not admin user
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@user.com', name='user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_delete_forbidden(self):
        """
        test retrieve country if not authenticated
        """
        country = models.Country.objects.create(name='country', code=1)
        url = retrieve_country_url(country.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
