from google.protobuf import reflection as _reflection

import logging
import os
import re

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)


class ControllerServiceRequest:
    def __init__(self, service=None, pb2=None, grpc_pb2=None, response_topic=None):
        self.service = service
        self.pb2 = pb2
        self.grpc_pb2 = grpc_pb2
        self.response_topic = response_topic


controller_service = []


def add_controller_service(service=None, pb2=None, grpc_pb2=None, response_topic=None):
    controller_service.append(
        ControllerServiceRequest(service=service, grpc_pb2=grpc_pb2, pb2=pb2, response_topic=response_topic))


def process_request(message=bytes):
    logging.info("############ CommandHandler process_request ##########")

    r = re.match('^([A-Za-z]+).([A-Za-z]+):([A-Za-z]+)$', message.key.decode())

    if not r:
        logging.error(f'Error: Message Format Mismatch! {message.key.decode()}')
        return

    request_controller = r.group(1)
    request_action = r.group(2)
    request_message_type = r.group(3)

    for controller_service_request in controller_service:
        try:

            if request_controller not in controller_service_request.pb2.DESCRIPTOR.services_by_name.keys():
                logging.error(f'Error: Request Controller not found! {request_controller}')
                continue

            service_method = controller_service_request.pb2.DESCRIPTOR.services_by_name[
                request_controller].FindMethodByName(request_action)

            if not service_method:
                logging.error(f'Error: Request Method not found! {request_action}')
                continue

            if service_method.input_type.name != request_message_type:
                logging.error(f'Error: Mismatch {service_method.input_type.name} {request_message_type}')
                continue

            obj = _reflection.ParseMessage(service_method.input_type, message.value)
            service = controller_service_request.service

            if hasattr(service, request_action) and callable(getattr(service, request_action)):
                logging.info("process_request is executing...")
                try:
                    servicer = service.as_servicer()
                    response = servicer.__getattr__(request_action)(obj, None)

                    if service_method.output_type.name != response.__class__.__name__:
                        raise Exception(
                            f'Response should be of {service_method.output_type.name} type. {response.__class__.__name__} type returned!')

                    producer = KafkaProducer(bootstrap_servers=os.environ.get('BOOTSTRAP_SERVERS'))
                    producer.send(topic=controller_service_request.response_topic,
                                  key=bytes(f'{request_controller}.Response:{service_method.output_type.name}',
                                            'utf-8'),
                                  value=response.SerializeToString())
                    logging.info("process_request complete!")

                except Exception as ex:
                    logging.error(ex)

        except Exception as e:
            logging.error(e)
            continue
