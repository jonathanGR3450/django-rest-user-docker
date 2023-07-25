from core import models


def sample_country(name='country 1', code=1):
    country = models.Country.objects.create(name=name, code=code)
    return country


def sample_state(name='state 1', code=1):
    country = sample_country()
    state = models.State.objects.create(name=name, code=code, country=country)
    return state


def sample_city(name='city', code=1):
    state = sample_state()
    city = models.City.objects.create(name=name, code=code, state=state)
    return city
