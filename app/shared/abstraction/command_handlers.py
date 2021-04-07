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


class DelegatorServiceRequest:
    def __init__(self, pb2=None, grpc_pb2=None, response_topics=[]):
        self.pb2 = pb2
        self.grpc_pb2 = grpc_pb2
        self.response_topics = response_topics


controller_service = []
delegator_service = {}


def add_delegator_service(key=None, delegate_topics=[]):
    r = re.match('^Response:([A-Za-z]+).([A-Za-z]+):([A-Za-z]+)$', key)
    if not r:
        raise Exception(f'Delegator key format mismatch!')

    delegator_service[key] = delegate_topics


def add_controller_service(service=None, pb2=None, grpc_pb2=None, response_topic=None):
    response_topic = os.environ.get('SERVICE_TOPIC') if response_topic is None else response_topic
    controller_service.append(
        ControllerServiceRequest(service=service, grpc_pb2=grpc_pb2, pb2=pb2, response_topic=response_topic))


def delegator_request(message=bytes):
    logging.info("############ DelegatorHandler process_request ##########")
    key = message.key.decode()
    r = re.match('^Response:([A-Za-z]+).([A-Za-z]+):([A-Za-z]+)$', key)

    if not r:
        return

    if key not in delegator_service.keys():
        return

    request_controller = r.group(1)
    request_action = r.group(2)
    request_message_type = r.group(3)

    delegate_topics = delegator_service[key]
    for topic in delegate_topics:
        producer = KafkaProducer(bootstrap_servers=os.environ.get('BOOTSTRAP_SERVERS'))
        producer.send(topic=topic,
                      key=bytes(
                          f'{request_controller}.{request_action}:{request_message_type}',
                          'utf-8'),
                      value=message.value)


def process_request(message=bytes):
    logging.info("############ CommandHandler process_request ##########")

    r = re.match('^([A-Za-z]+).([A-Za-z]+):([A-Za-z]+)$', message.key.decode())

    if not r:
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
                                  key=bytes(
                                      f'Response:{request_controller}.{request_action}:{service_method.output_type.name}',
                                      'utf-8'),
                                  value=response.SerializeToString())
                    logging.info("process_request complete!")

                except Exception as ex:
                    logging.error(ex)

        except Exception as e:
            logging.error(e)
            continue
