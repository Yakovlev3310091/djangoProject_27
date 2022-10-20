import pytest


@pytest.fixture
@pytest.mark.django_db
def hr_token(client, django_user_model):
    username = "hr"
    password = "12345"

    django_user_model.objects.create_user(                  # создали django-пользователя
        username=username, password=password, role="hr"
    )

    response = client.post(                                # Авторизовались
        "/user/login/",
        {"username": username, "password": password},
        format='json'    # альтернатива - content_type="application/json" из vacancy_create_test (29 строка)
    )

    return response.data["token"]                      # Вытащили токен


