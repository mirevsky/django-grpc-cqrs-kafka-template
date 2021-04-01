import shared.abstraction.command_handlers as command_handlers

from shared.library.component_a.command import person_pb2, person_pb2_grpc
from component_a.command.services import PersonCommandService


def kafka_handlers():
    command_handlers.add_controller_service(grpc_pb2=person_pb2_grpc, pb2=person_pb2,
                                            service=PersonCommandService,
                                            response_topic='topic_component_a_command_response')
