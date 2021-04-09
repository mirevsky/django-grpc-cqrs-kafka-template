import grpc
from google.protobuf import empty_pb2
from django_grpc_framework.services import Service

from component_b.common.serializers import PersonProtoSerializer
from component_b.common.models import PersonModel


class PersonCommandService(Service):

    def get_object(self, pk):
        try:
            return PersonModel.objects.get(pk=pk)
        except PersonModel.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Post:%s not found!' % pk)

    def Create(self, request, context):
        serializer = PersonProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Update(self, request, context):
        post = self.get_object(request.id)
        serializer = PersonProtoSerializer(post, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Destroy(self, request, context):
        post = self.get_object(request.id)
        post.delete()
        return empty_pb2.Empty()
