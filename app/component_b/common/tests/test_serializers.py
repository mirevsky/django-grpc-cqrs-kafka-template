import pytest

from component_b.common.tests.fixtures import *
from component_b.common.models import PersonModel
from component_b.common.serializers import PersonProtoSerializer
from shared.library.component_b.common import person_message_pb2


@pytest.mark.django_db
class TestPersonProtoSerializer:

    def test_person_proto_serializer_query(self, mock_product, snapshot):
        queryset = PersonModel.objects.all()
        serializer = PersonProtoSerializer(queryset, many=True)
        assert serializer.data == snapshot

    def test_person_proto_serializer_validate(self, mock_product, snapshot):
        serializer = PersonProtoSerializer(
            message=person_message_pb2.Person(query='Test serializer validation', page_number=1, result_per_page=1))
        serializer.is_valid()
        assert serializer.data == snapshot
