import pytest
from django.urls import reverse

from my_auth.models import User

user_data = {
        'email': 'testmail@mail.com',
        'password': '12345678+',
        'password2': '12345678+',
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
}

login_credentials = {
        'email': 'testmail@mail.com',
        'password': '12345678+',
}

url_register = reverse('auth_register')
url_login = reverse('token_obtain_pair')
url_logout = reverse('auth_logout')
url_change_pass = '/auth/change_password/'
url_update_user = '/auth/update_user/'
url_get_user = '/auth/users/'


@pytest.mark.django_db
def test_register_user_success(client):
    response = client.post(url_register, user_data)
    data = response.data

    assert data['email'] == user_data['email']
    assert 'password' not in data
    assert 'password2' not in data
    assert data['first_name'] == user_data['first_name']
    assert data['last_name'] == user_data['last_name']


@pytest.mark.django_db
def test_should_not_register_passwords_do_not_match(client):
    this_payload = user_data.copy()
    this_payload['password2'] = '12345679+'
    response = client.post(url_register, this_payload)
    data = response.data

    assert response.status_code == 400
    assert 'password' in data
    error = str(data['password'][0])
    assert error == 'Password fields do not match'


@pytest.mark.django_db
def test_should_not_register_user_with_existing_email(client):
    client.post(url_register, user_data)
    response = client.post(url_register, user_data)
    data = response.data

    assert response.status_code == 400
    assert 'email' in data
    error = str(data['email'][0])
    assert error == 'This field must be unique.'


@pytest.mark.django_db
def test_login_user_success(client):
    client.post(url_register, user_data)
    response = client.post(url_login, login_credentials)
    data = response.data

    assert response.status_code == 200
    assert 'access' in data
    assert 'refresh' in data
    assert 'user' in data
    assert 'id' in data['user']
    assert 'email' in data['user']
    assert 'first_name' in data['user']
    assert 'last_name' in data['user']


@pytest.mark.django_db
def test_login_with_wrong_email(client):
    client.post(url_register, user_data)
    this_login_credentials = login_credentials.copy()
    this_login_credentials['email'] = 'wrong@mail.com'
    response = client.post(url_login, this_login_credentials)
    data = response.data

    assert response.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'No active account found with the given credentials'


@pytest.mark.django_db
def test_login_with_wrong_password(client):
    client.post(url_register, user_data)
    this_login_credentials = login_credentials.copy()
    this_login_credentials['password'] = 'wrong'
    response = client.post(url_login, this_login_credentials)
    data = response.data

    assert response.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'No active account found with the given credentials'


@pytest.mark.django_db
def test_login_with_missing_email(client):
    client.post(url_register, user_data)
    this_login_credentials = login_credentials.copy()
    del this_login_credentials['email']
    response = client.post(url_login, this_login_credentials)
    data = response.data

    assert response.status_code == 400
    assert 'email' in data
    error = str(data['email'][0])
    assert error == 'This field is required.'


@pytest.mark.django_db
def test_login_with_missing_password(client):
    client.post(url_register, user_data)
    this_login_credentials = login_credentials.copy()
    del this_login_credentials['password']
    response = client.post(url_login, this_login_credentials)
    data = response.data

    assert response.status_code == 400
    assert 'password' in data
    error = str(data['password'][0])
    assert error == 'This field is required.'


@pytest.mark.django_db
def test_change_password_success(client):
    payload = {
      "old_password": user_data['password'],
      "password": '12345679+',
      "password2": '12345679+'
    }
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    client.force_authenticate(user=user)
    url = url_change_pass + str(user.pk) + '/'
    response = client.put(url, payload)

    assert response.status_code == 200


@pytest.mark.django_db
def test_should_not_be_able_change_password_of_another_user(client):
    payload = {
        "old_password": user_data['password'],
        "password": 'newpass+',
        "password2": 'newpass+'
    }
    user2_data = user_data.copy()
    user2_data['email'] = 'second@mail.com'
    client.post(url_register, user_data)
    client.post(url_register, user2_data)
    user1 = User.objects.get(email=user_data['email'])
    user2 = User.objects.get(email=user2_data['email'])
    client.force_authenticate(user=user1)
    url = url_change_pass + str(user2.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 403
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'You do not have permission to perform this action.'


@pytest.mark.django_db
def test_should_not_be_able_change_password_unauthenticated(client):
    payload = {
        "old_password": user_data['password'],
        "password": '12345679+',
        "password2": '12345679+'
    }
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    url = url_change_pass + str(user.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_should_not_be_able_change_password_with_wrong_old_password(client):
    payload = {
        "old_password": 'wrongpass',
        "password": '12345679+',
        "password2": '12345679+'
    }
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    client.force_authenticate(user=user)
    url = url_change_pass + str(user.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 400
    assert 'old_password' in data
    error = str(data['old_password'][0])
    assert error == 'Old password is not correct.'


@pytest.mark.django_db
def test_should_not_be_able_change_password_new_passwords_do_not_match(client):
    payload = {
        "old_password": user_data['password'],
        "password": '12345679+',
        "password2": 'wrong'
    }
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    client.force_authenticate(user=user)
    url = url_change_pass + str(user.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 400
    assert 'password' in data
    error = str(data['password'][0])
    assert error == 'Password fields do not match.'


@pytest.mark.django_db
def test_update_user_info_success(client):
    payload = {
        'email': 'newmail@mail.com',
        'first_name': 'new_name',
        'last_name': 'new_last_name',
    }

    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    client.force_authenticate(user=user)
    url = url_update_user + str(user.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 200
    assert 'email' in data
    assert 'first_name' in data
    assert 'last_name' in data
    assert data['email'] == payload['email']
    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']


@pytest.mark.django_db
def test_should_not_be_able_to_update_another_user(client):
    payload = {
        'email': 'newmail@mail.com',
        'first_name': 'new_name',
        'last_name': 'new_last_name',
    }
    user2_data = user_data.copy()
    user2_data['email'] = 'second@mail.com'
    client.post(url_register, user_data)
    client.post(url_register, user2_data)
    user1 = User.objects.get(email=user_data['email'])
    user2 = User.objects.get(email=user2_data['email'])
    client.force_authenticate(user=user1)
    url = url_update_user + str(user2.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 400
    assert 'authorization' in data
    error = str(data['authorization'])
    assert error == 'You do not have permission for this user.'


@pytest.mark.django_db
def test_should_not_be_able_to_update_user_info_unauthenticated(client):
    payload = {
        'email': 'newmail@mail.com',
        'first_name': 'new_name',
        'last_name': 'new_last_name',
    }
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    url = url_update_user + str(user.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_should_not_be_able_to_use_another_user_email(client):
    payload = {
        'email': user_data['email'],
        'first_name': 'new_name',
        'last_name': 'new_last_name',
    }
    user2_data = user_data.copy()
    user2_data['email'] = 'second@mail.com'
    client.post(url_register, user_data)
    client.post(url_register, user2_data)
    user1 = User.objects.get(email=user_data['email'])
    user2 = User.objects.get(email=user2_data['email'])
    client.force_authenticate(user=user2)
    url = url_update_user + str(user2.pk) + '/'
    response = client.put(url, payload)
    data = response.data

    assert response.status_code == 400
    assert 'email' in data
    error = str(data['email'][0])
    assert error == 'This email is already in use.'


@pytest.mark.django_db
def test_logout_success(client):
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    credentials = client.post(url_login, login_credentials)
    data = credentials.data
    client.force_authenticate(user=user)
    response = client.post(url_logout, data={'refresh_token': data['refresh']})

    assert response.status_code == 205


@pytest.mark.django_db
def test_should_not_be_able_to_logout_unauthenticated(client):
    client.post(url_register, user_data)
    User.objects.get(email=user_data['email'])
    credentials = client.post(url_login, login_credentials)
    credentials_data = credentials.data
    response = client.post(url_logout, data={'refresh_token': credentials_data['refresh']})
    data = response.data

    assert response.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_get_user_info_success(client):
    client.post(url_register, user_data)
    user = User.objects.get(email=user_data['email'])
    url = url_get_user + str(user.pk) + '/'
    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert 'pk' in data
    assert 'first_name' in data
    assert 'last_name' in data
    assert 'date_joined' in data
    assert 'last_login' in data
    assert data['pk'] == str(user.pk)
    assert data['first_name'] == user_data['first_name']
    assert data['last_name'] == user_data['last_name']


@pytest.mark.django_db
def test_should_only_be_able_to_get_single_user(client):
    response = client.get(url_get_user)

    assert response.status_code == 404
