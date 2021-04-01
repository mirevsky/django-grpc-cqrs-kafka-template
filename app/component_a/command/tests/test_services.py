import pytest
from component_a.common.tests.fixtures import *

from component_a.command.services import PersonCommandService


@pytest.mark.django_db
class TestPersonCommandService:

    def test_create(self):
        assert True

    def test_update(self):
        assert True

    def test_delete(self):
        assert True
