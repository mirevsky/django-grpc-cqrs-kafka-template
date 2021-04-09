import pytest
from component_b.common.tests.fixtures import *

from component_b.command.services import PersonCommandService


@pytest.mark.django_db
class TestPersonCommandService:

    def test_create(self):
        assert True

    def test_update(self):
        assert True

    def test_delete(self):
        assert True
