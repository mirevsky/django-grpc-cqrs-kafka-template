import os
import shared.abstraction.command_controller as command_controller
import shared.abstraction.command_handlers as command_handlers

from component_a.command.handlers import kafka_handlers


class DomainCommandController(command_controller.CommandController):

    def process_command(self, message):
        kafka_handlers()
        command_handlers.process_request(message=message)


if __name__ == '__main__':
    controller = DomainCommandController(topic=os.environ.get('SERVICE_TOPIC'),
                                         bootstrap_servers=os.environ.get('BOOTSTRAP_SERVERS'))
    controller.run()
