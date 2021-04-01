import pytest

from component_a.common.models import PersonModel


@pytest.mark.django_db
class TestPersonModel:

    def test_person_model(self):
        person = PersonModel(query="Test person", page_number=1, result_per_page=1)
        person.save()
        assert person.id != None