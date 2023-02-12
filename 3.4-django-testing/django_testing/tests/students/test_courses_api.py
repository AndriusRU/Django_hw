from django.urls import reverse
from rest_framework.test import APIClient
import pytest
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    make_course = course_factory(_quantity=1)
    first = make_course[0]
    response = client.get(f'/api/v1/courses/{first.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == first.name


@pytest.mark.django_db
def test_get_all_course(client, course_factory):
    make_course = course_factory(_quantity=12)
    response = client.get(f'/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for i, num in enumerate(data):
        assert num['name'] == make_course[i].name


@pytest.mark.django_db
def test_get_filter_course_id(client, course_factory):
    make_course = course_factory(_quantity=1)
    # response = client.get(f'/api/v1/courses/', {'id': make_course[0].id})
    response = client.get(f'/api/v1/courses/?id={make_course[0].id}')

    assert response.status_code == 200
    data = response.json()
    assert make_course[0].id == data[0]['id']


@pytest.mark.django_db
def test_get_filter_course_name(client, course_factory):
    make_course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/', {'name': make_course[0].name})
    # response = client.get(f'/api/v1/courses/?name={make_course[0].name}')

    assert response.status_code == 200
    data = response.json()
    assert make_course[0].name == data[0]['name']


@pytest.mark.django_db
def test_create_course(client):
    response = client.post(reverse('courses-list'), data={
        'name': 'django'
    })
    assert response.status_code == 201
    data = response.json()
    assert Course.objects.get(id=data['id']).name == data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    my_course = course_factory(_quantity=1)
    response = client.patch(reverse('courses-detail', args=[my_course[0].id]), data={
        'name': 'django'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'django'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    my_course = course_factory(_quantity=1)
    response = client.delete(reverse('courses-detail', args=[my_course[0].id]))
    assert response.status_code == 204

