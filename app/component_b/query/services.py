import grpc
from django_grpc_framework import generics
from django_grpc_framework.services import Service

from component_b.common.models import PersonModel
from component_b.common.serializers import PersonProtoSerializer


class PersonQueryService(Service):

    def get_object(self, pk):
        try:
            return PersonModel.objects.get(pk=pk)
        except PersonModel.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Post:%s not found!' % pk)

    def List(self, request, context):
        serializer = PersonProtoSerializer(PersonModel.objects.all(), many=True)
        for msg in serializer.message:
            yield msg

    def Retrieve(self, request, context):
        post = self.get_object(request.id)
        serializer = PersonProtoSerializer(post)
        return serializer.message
