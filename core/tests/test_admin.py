from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


class AdminSiteTests(TestCase):
    """ clase para pobar el admin de django """

    def setUp(self):
        self.user_admin = get_user_model().objects.create_superuser(
            email='admin@admin.com',
            password='test123'
        )
        self.client = Client()
        self.client.force_login(self.user_admin)
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test123',
            name='name'
        )

    def test_list_users(self):
        ''' probar listar usuarios '''
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)
        self.assertContains(response, self.user.name)

    def test_user_change_page(self):
        ''' probar pagina de actualizar usuario '''
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
