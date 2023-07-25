from django.test import TestCase
from core.models import Country, State, City
from django.contrib.auth import get_user_model


def sampleUser(email='test@test.com', password='password'):
    ''' crea un usuario '''
    return get_user_model().objects.create_user(email=email, password=password)


class TestsModels(TestCase):
    """ purebas para los modelos """

    def test_create_user(self):
        ''' prueba crear modelo usuario '''
        email = 'test@test.com'
        password = 'test124'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        ''' probar normalizacion de correo '''
        email = 'test@TEST.COM'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_user_without_email(self):
        ''' prueba usuario sin correo '''
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(email='', password='test')

    def test_create_superuser(self):
        ''' crear super usuario '''
        email = 'test@test.com'
        password = 'test1234'
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_without_password(self):
        ''' crear super usuario sin contrase~na '''
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_superuser(email='test@test.com', password=None)

    def test_listed_users(self):
        ''' listar usuarios '''
        user = get_user_model().objects.create_user(email='test@test.com', password='password')
        users = get_user_model().objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, user.email)

    def test_country_str(self):
        """
        test country str
        """
        country = Country.objects.create(
            name='country',
            code=1
        )
        self.assertEqual(str(country), country.name)

    def test_state_str(self):
        """
        test state str
        """
        country = Country.objects.create(name='country', code=1)
        state = State.objects.create(name='state', code=1, country=country)
        self.assertEqual(str(state), state.name)

    def test_city_str(self):
        """
        test city str
        """
        country = Country.objects.create(name='country', code=1)
        state = State.objects.create(name='state', code=1, country=country)
        city = City.objects.create(name='city', code=1, state=state)
        self.assertEqual(str(city), city.name)
