import shared.abstraction.command_handlers as command_handlers

from shared.library.component_a.command import person_pb2, person_pb2_grpc
from component_a.command.services import PersonCommandService


def kafka_handlers():
    command_handlers.add_controller_service(grpc_pb2=person_pb2_grpc, pb2=person_pb2,
                                            service=PersonCommandService,
                                            response_topic='topic_component_a_command_response')


def delegator_handlers():
    command_handlers.add_delegator_service(key='Response:PersonController.Create:Person',
                                           delegate_topics=['topic_component_b_command_response',
                                                            'topic_component_c_command_response'])
