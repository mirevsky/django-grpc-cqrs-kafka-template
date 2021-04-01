import pytest

from integration_tests.component_a.fixtures import *

@pytest.mark.django_db
class TestDomainQueryController():

    def test_list(self):
        assert True

    def test_retrieve(self):
        assert True
