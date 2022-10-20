import factory.django

from authentication.models import User
from vacancies.models import Vacancy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    #username = "test"
    username = factory.Faker("name")
    password = "12345"


class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy

    slug = "test"
    text = "test text"
    user = factory.SubFactory(UserFactory)

