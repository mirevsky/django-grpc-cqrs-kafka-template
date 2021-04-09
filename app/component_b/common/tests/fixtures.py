import pytest

from django.test import Client

from component_b.common.models import PersonModel


@pytest.fixture(scope="session")
def api_client():
    return Client(HTTP_USER_AGENT="django-test-api-client")


@pytest.fixture(scope="function")
def mock_product():
    product = PersonModel.objects.create(query='Test product', page_number=1, result_per_page=1)
    return product

@pytest.fixture(scope="function")
def mock_products():
    PersonModel.objects.create(query='Test product 1', page_number=1, result_per_page=1)
    PersonModel.objects.create(query='Test product 2', page_number=1, result_per_page=1)
    return PersonModel.objects.all()
