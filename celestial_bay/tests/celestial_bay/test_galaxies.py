import pytest
from django.urls import reverse

from my_auth.models import User
from galaxies.models import Constellation, ConstellationImage, Galaxy


url_constellations = '/constellations/'
url_constellation_images = '/constellation_images/'
url_galaxies = '/galaxies/'
url_galaxy_images = '/galaxy_images/'
url_posts = '/posts/'
url_post_images = '/post_images/'
url_comments = '/comments/'

constellation_data = {
    'name': 'name1',
    'abbreviation': 'ab1',
    'area_in_sq_deg': '111',
}
user_data = {
        'email': 'testmail@mail.com',
        'password': '12345678+',
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
}
login_credentials = {
        'email': 'testmail@mail.com',
        'password': '12345678+',
}
galaxy_data = {
    "name": "name1",
    "name_origin": "origin1",
    "notes": "note1",
    "galaxy_type": "type1",
    "distance": 11,
    "apparent_magnitude": 11,
    "size": 11,
}


@pytest.mark.django_db
def test_get_all_constellations_success(client):
    constellations = (
        {
            'name': 'name1',
            'abbreviation': 'ab1',
            'area_in_sq_deg': '111',
        },
        {
            'name': 'name2',
            'abbreviation': 'ab2',
            'area_in_sq_deg': '222',
        },
        {
            'name': 'name3',
            'abbreviation': 'ab3',
            'area_in_sq_deg': '333',
        },

    )

    Constellation.objects.create(**constellations[0])
    Constellation.objects.create(**constellations[1])
    Constellation.objects.create(**constellations[2])

    request = client.get(url_constellations)
    data = request.data

    assert request.status_code == 200
    assert 'count' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data
    assert data['count'] == 3
    assert len(data['results']) == 3

    results = data['results']

    for i in range(len(results)):
        assert 'pk' in results[i]
        assert 'name' in results[i]
        assert 'abbreviation' in results[i]
        assert 'area_in_sq_deg' in results[i]
        assert results[i]['pk'] == i + 1
        assert results[i]['name'] == constellations[i]['name']
        assert results[i]['abbreviation'] == constellations[i]['abbreviation']
        assert results[i]['area_in_sq_deg'] == float(constellations[i]['area_in_sq_deg'])


@pytest.mark.django_db
def test_get_constellation_by_id_success(client):
    constellations = (
        {
            'name': 'name1',
            'abbreviation': 'ab1',
            'area_in_sq_deg': '111',
        },
        {
            'name': 'name2',
            'abbreviation': 'ab2',
            'area_in_sq_deg': '222',
        },
        {
            'name': 'name3',
            'abbreviation': 'ab3',
            'area_in_sq_deg': '333',
        },

    )

    Constellation.objects.create(**constellations[0])
    constellation = Constellation.objects.create(**constellations[1])
    Constellation.objects.create(**constellations[2])

    request = client.get(url_constellations + str(constellation.pk) + '/')
    data = request.data

    assert 'pk' in data
    assert 'name' in data
    assert 'abbreviation' in data
    assert 'area_in_sq_deg' in data
    assert data['pk'] == constellation.pk
    assert data['name'] == constellations[1]['name']
    assert data['abbreviation'] == constellations[1]['abbreviation']
    assert data['area_in_sq_deg'] == float(constellations[1]['area_in_sq_deg'])


@pytest.mark.django_db
def test_get_constellation_image_by_id_success(client):
    constellation = Constellation.objects.create(
        name='name1',
        abbreviation='ab1',
        area_in_sq_deg='111'
    )
    ConstellationImage.objects.create(
        constellation=constellation
    )

    request = client.get(url_constellation_images + '1' + '/')

    assert request.status_code == 200


@pytest.mark.django_db
def test_create_galaxy_success(client):
    constellation = Constellation.objects.create(**constellation_data)
    user = User.objects.create(**user_data)
    client.force_authenticate(user=user)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['constellation'] = constellation.pk
    this_galaxy_data['owner'] = user.pk
    request = client.post(url_galaxies, this_galaxy_data)
    data = request.data

    assert request.status_code == 201
    assert 'pk' in data
    assert 'name' in data
    assert 'name_origin' in data
    assert 'notes' in data
    assert 'galaxy_type' in data
    assert 'distance' in data
    assert 'apparent_magnitude' in data
    assert 'size' in data
    assert 'owner' in data
    assert 'constellation' in data
    assert data['pk'] == 1
    assert data['name'] == this_galaxy_data['name']
    assert data['name_origin'] == this_galaxy_data['name_origin']
    assert data['notes'] == this_galaxy_data['notes']
    assert data['galaxy_type'] == this_galaxy_data['galaxy_type']
    assert data['distance'] == this_galaxy_data['distance']
    assert data['apparent_magnitude'] == this_galaxy_data['apparent_magnitude']
    assert data['size'] == this_galaxy_data['size']
    assert data['owner'] == this_galaxy_data['owner']
    assert data['constellation'] == this_galaxy_data['constellation']


@pytest.mark.django_db
def test_list_galaxy_success(client):
    constellation, user =\
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    galaxy1_data, galaxy2_data = galaxy_data.copy(), galaxy_data.copy()
    galaxy1_data['owner'], galaxy1_data['constellation'] = user, constellation
    galaxy2_data['name'], galaxy2_data['owner'], galaxy2_data['constellation'] =\
        'galaxy2', user, constellation
    galaxies = [Galaxy.objects.create(**galaxy1_data), Galaxy.objects.create(**galaxy2_data)]
    request = client.get(url_galaxies)
    data = request.data

    assert request.status_code == 200
    assert 'count' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data
    assert data['count'] == 2
    assert len(data['results']) == 2

    results = data['results']

    for i in range(len(results)):
        assert 'pk' in results[i]
        assert 'name' in results[i]
        assert 'name_origin' in results[i]
        assert 'notes' in results[i]
        assert 'galaxy_type' in results[i]
        assert 'distance' in results[i]
        assert 'apparent_magnitude' in results[i]
        assert 'size' in results[i]
        assert 'owner' in results[i]
        assert 'constellation' in results[i]
        assert results[i]['pk'] == galaxies[i].pk
        assert results[i]['name'] == galaxies[i].name
        assert results[i]['name_origin'] == galaxies[i].name_origin
        assert results[i]['notes'] == galaxies[i].notes
        assert results[i]['galaxy_type'] == galaxies[i].galaxy_type
        assert results[i]['distance'] == galaxies[i].distance
        assert results[i]['apparent_magnitude'] == galaxies[i].apparent_magnitude
        assert results[i]['size'] == galaxies[i].size
        assert results[i]['owner'] == galaxies[i].owner.pk
        assert results[i]['constellation'] == galaxies[i].constellation.pk


@pytest.mark.django_db
def test_retrieve_galaxy_success(client):
    constellation, user =\
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    galaxy1_data, galaxy2_data, galaxy3_data =\
        galaxy_data.copy(), galaxy_data.copy(), galaxy_data.copy()
    galaxy1_data['owner'], galaxy1_data['constellation'] = user, constellation
    galaxy2_data['name'], galaxy2_data['owner'], galaxy2_data['constellation'] =\
        'galaxy2', user, constellation
    galaxy3_data['name'], galaxy3_data['owner'], galaxy3_data['constellation'] =\
        'galaxy3', user, constellation
    Galaxy.objects.create(**galaxy1_data)
    galaxy2 = Galaxy.objects.create(**galaxy2_data)
    Galaxy.objects.create(**galaxy3_data)

    request = client.get(url_galaxies + str(galaxy2.pk) + '/')
    data = request.data

    assert request.status_code == 200

    assert 'pk' in data
    assert 'name' in data
    assert 'name_origin' in data
    assert 'notes' in data
    assert 'galaxy_type' in data
    assert 'distance' in data
    assert 'apparent_magnitude' in data
    assert 'size' in data
    assert 'owner' in data
    assert 'constellation' in data
    assert data['pk'] == galaxy2.pk
    assert data['name'] == galaxy2_data['name']
    assert data['name_origin'] == galaxy2_data['name_origin']
    assert data['notes'] == galaxy2_data['notes']
    assert data['galaxy_type'] == galaxy2_data['galaxy_type']
    assert data['distance'] == galaxy2_data['distance']
    assert data['apparent_magnitude'] == galaxy2_data['apparent_magnitude']
    assert data['size'] == galaxy2_data['size']
    assert data['owner'] == galaxy2_data['owner'].pk
    assert data['constellation'] == galaxy2_data['constellation'].pk


@pytest.mark.django_db
def test_update_galaxy_success(client):
    constellation, user =\
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    client.force_authenticate(user=user)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    update_data = this_galaxy_data.copy()
    update_data['name_origin'] = 'new_origin'
    update_data['notes'] = 'new_notes'
    update_data['owner'] = galaxy.owner.pk
    update_data['constellation'] = galaxy.constellation.pk
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.put(url, update_data)
    data = request.data

    assert request.status_code == 200
    assert 'pk' in data
    assert 'name' in data
    assert 'name_origin' in data
    assert 'notes' in data
    assert 'galaxy_type' in data
    assert 'distance' in data
    assert 'apparent_magnitude' in data
    assert 'size' in data
    assert 'owner' in data
    assert 'constellation' in data
    assert data['pk'] == galaxy.pk
    assert data['name'] == galaxy_data['name']
    assert data['name_origin'] == update_data['name_origin']
    assert data['notes'] == update_data['notes']
    assert data['galaxy_type'] == galaxy_data['galaxy_type']
    assert data['distance'] == galaxy_data['distance']
    assert data['apparent_magnitude'] == galaxy_data['apparent_magnitude']
    assert data['size'] == galaxy_data['size']
    assert data['owner'] == galaxy.owner.pk
    assert data['constellation'] == galaxy.constellation.pk


@pytest.mark.django_db
def test_partial_update_galaxy_success(client):
    constellation, user = \
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    client.force_authenticate(user=user)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    update_data = {'name': 'new_name', 'size': 303}
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.patch(url, update_data)
    data = request.data

    assert request.status_code == 200
    assert 'pk' in data
    assert 'name' in data
    assert 'name_origin' in data
    assert 'notes' in data
    assert 'galaxy_type' in data
    assert 'distance' in data
    assert 'apparent_magnitude' in data
    assert 'size' in data
    assert 'owner' in data
    assert 'constellation' in data
    assert data['pk'] == galaxy.pk
    assert data['name'] == update_data['name']
    assert data['name_origin'] == galaxy.name_origin
    assert data['notes'] == galaxy.notes
    assert data['galaxy_type'] == galaxy.galaxy_type
    assert data['distance'] == galaxy.distance
    assert data['apparent_magnitude'] == galaxy.apparent_magnitude
    assert data['size'] == update_data['size']
    assert data['owner'] == galaxy.owner.pk
    assert data['constellation'] == galaxy.constellation.pk


@pytest.mark.django_db
def test_delete_galaxy_success(client):
    constellation, user = \
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    client.force_authenticate(user=user)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.delete(url)

    assert request.status_code == 204


@pytest.mark.django_db
def test_not_able_create_galaxy_when_unauthenticated(client):
    constellation = Constellation.objects.create(**constellation_data)
    user = User.objects.create(**user_data)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['constellation'] = constellation.pk
    this_galaxy_data['owner'] = user.pk
    request = client.post(url_galaxies, this_galaxy_data)
    data = request.data

    assert request.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_not_able_to_create_galaxy_when_name_in_use(client):
    constellation = Constellation.objects.create(**constellation_data)
    user = User.objects.create(**user_data)
    client.force_authenticate(user=user)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['constellation'] = constellation.pk
    this_galaxy_data['owner'] = user.pk
    client.post(url_galaxies, this_galaxy_data)
    request = client.post(url_galaxies, this_galaxy_data)
    data = request.data

    assert request.status_code == 400
    assert 'name' in data
    error = str(data['name'][0])
    assert error == 'galaxy with this name already exists.'


@pytest.mark.django_db
def test_not_able_to_update_galaxy_when_unauthenticated(client):
    constellation, user = \
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    update_data = {'name': 'new_name', 'size': 303}
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.patch(url, update_data)
    data = request.data

    assert request.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_not_able_to_delete_galaxy_when_unauthenticated(client):
    constellation, user = \
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.delete(url)
    data = request.data

    assert request.status_code == 401
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_not_able_to_update_galaxy_when_not_owner(client):
    constellation, user = \
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    user2_data = user_data.copy()
    user2_data['email'] = 'user2@mail.com'
    user2 = User.objects.create(**user2_data)
    client.force_authenticate(user=user2)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    update_data = {'name': 'new_name', 'size': 303}
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.patch(url, update_data)
    data = request.data

    assert request.status_code == 403
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'You do not have permission to perform this action.'


@pytest.mark.django_db
def test_not_able_to_delete_galaxy_when_not_owner(client):
    constellation, user = \
        Constellation.objects.create(**constellation_data), User.objects.create(**user_data)
    user2_data = user_data.copy()
    user2_data['email'] = 'user2@mail.com'
    user2 = User.objects.create(**user2_data)
    client.force_authenticate(user=user2)
    this_galaxy_data = galaxy_data.copy()
    this_galaxy_data['owner'] = user
    this_galaxy_data['constellation'] = constellation
    galaxy = Galaxy.objects.create(**this_galaxy_data)
    url = url_galaxies + str(galaxy.pk) + '/'
    request = client.delete(url)
    data = request.data

    assert request.status_code == 403
    assert 'detail' in data
    error = str(data['detail'])
    assert error == 'You do not have permission to perform this action.'


@pytest.mark.django_db
def test_create__success(client):
    pass


@pytest.mark.django_db
def test_list__success(client):
    pass


@pytest.mark.django_db
def test_retrieve__success(client):
    pass


@pytest.mark.django_db
def test_update__success(client):
    pass


@pytest.mark.django_db
def test_partial_update__success(client):
    pass


@pytest.mark.django_db
def test_delete__success(client):
    pass


@pytest.mark.django_db
def test_not_able_create__when_unauthenticated(client):
    pass


@pytest.mark.django_db
def test_not_able_to_create__when_name_in_use(client):
    pass


@pytest.mark.django_db
def test_not_able_to_update__when_unauthenticated(client):
    pass


@pytest.mark.django_db
def test_not_able_to_delete__when_unauthenticated(client):
    pass


@pytest.mark.django_db
def test_not_able_to_update__when_not_owner(client):
    pass


@pytest.mark.django_db
def test_not_able_to_delete__when_not_owner(client):
    pass
