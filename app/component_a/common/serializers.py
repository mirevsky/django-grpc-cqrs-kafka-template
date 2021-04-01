from django_grpc_framework import proto_serializers

from shared.library.component_a.common import person_message_pb2
from component_a.common.models import PersonModel


class PersonProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = PersonModel
        proto_class = person_message_pb2.Person
        fields = '__all__'
