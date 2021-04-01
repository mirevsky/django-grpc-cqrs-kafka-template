import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()

from kafka import KafkaConsumer


class CommandController:

    def __init__(self, topic: str, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.logging = logging

    def process_command(self, message):
        logging.info("############ CommandController ##########")
        logging.info("IMPORTANT: process_command is not assigned in DomainCommandController!")


    def run(self):
        consumer = KafkaConsumer(self.topic,
                                 bootstrap_servers=self.bootstrap_servers.split(),
                                 enable_auto_commit=True,
                                 auto_offset_reset='earliest',
                                 api_version=(0, 10)
                                 )
        for event in consumer:
            self.process_command(event)
        sys.exit()
