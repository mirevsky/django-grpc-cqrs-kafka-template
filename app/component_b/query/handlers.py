from shared.library.component_b.query import person_pb2_grpc
from component_b.query.services import PersonQueryService


def grpc_handlers(server):
    person_pb2_grpc.add_PersonControllerServicer_to_server(PersonQueryService.as_servicer(), server)
