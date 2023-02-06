import pytest
from django.urls import reverse

from my_auth.models import User
from galaxies.models import Constellation, ConstellationImage


url_constellations = '/constellations/'
url_constellation_images = '/constellation_images/'
url_galaxies = '/galaxies/'

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
    Constellation.objects.create(**constellations[1])
    Constellation.objects.create(**constellations[2])

    request = client.get(url_constellations + '2' + '/')
    data = request.data

    assert 'pk' in data
    assert 'name' in data
    assert 'abbreviation' in data
    assert 'area_in_sq_deg' in data
    assert data['pk'] == 2
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
    pass


@pytest.mark.django_db
def test_retrieve_galaxy_success(client):
    pass


@pytest.mark.django_db
def test_update_galaxy_success(client):
    pass


@pytest.mark.django_db
def test_partial_update_galaxy_success(client):
    pass


@pytest.mark.django_db
def test_delete_galaxy_success(client):
    pass


@pytest.mark.django_db
def test_not_able_create_galaxy_when_unauthenticated(client):
    pass


@pytest.mark.django_db
def test_not_able_to_create_galaxy_when_name_in_use(client):
    pass


@pytest.mark.django_db
def test_not_able_to_update_galaxy_when_unauthenticated(client):
    pass


@pytest.mark.django_db
def test_not_able_to_delete_galaxy_when_unauthenticated(client):
    pass


@pytest.mark.django_db
def test_not_able_to_update_galaxy_when_not_owner(client):
    pass


@pytest.mark.django_db
def test_not_able_to_delete_galaxy_when_not_owner(client):
    pass


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
