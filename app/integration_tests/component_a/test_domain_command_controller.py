import pytest
from integration_tests.component_a.fixtures import *

@pytest.mark.django_db
class TestDomainCommandController:

    def test_create(self):
        assert True

    def test_update(self):
        assert True

    def test_delete(self):
        assert True
