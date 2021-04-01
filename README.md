# Emerald+ Micro-service Template
## Django GRPS Framework, Kafka, MySQL, Redis using CQRS Architecture

### Requirements

- RHEL 8.3, Fedora 33, CentOS 7
- Docker, Docker-compose

### Installation

```
chmod +x app.sh
./app.sh run local install
```

### Shell commands
```
 +----------------------------------------------------------------------------------------------+
 |                        ::.......................................:--                          |
 |                      :-:.....................................:--=+=                          |
 |                    .----:.................................::----=++=.                        |
 |                   .------:..............................:------=+++++:                       |
 |                  .--------:..........................::--------=++++++:                      |
 |                 :----------:.......................:-----------++++++++-                     |
 |                :-----------:.....................:------------=+++++++++-                    |
 |               :-------------:.................::--------------=++++++++++=                   |
 |              ----------------:..............:----------------=++++++++++++=.                 |
 |            .------------------:...........:------------------=+++++++++++++=.                |
 |           .--------------------:.......::--------------------++++++++++++++++:               |
 |          :---------------------:.....:----------------------=+++++++++++++++++:              |
 |         :-----------------------:..:------------------------=++++++++++++++++++-             |
 |        :---------------------------------------------------=++++++++++++++++++++-            |
 |       :--------------------------=+==----------------------=+++++++++++++++++++++=           |
 |      ---------------------------=++++==--------------------+++++++++++++++++++++++=.         |
 |    .----------------------------=++++++==-----------------=++++++++++++++++++++++++=.        |
 |   .----------------------------=++++++++++=---------------=++++++++++++++++++++++++++:       |
 |  .-----------------------------=++++++++++++==-----------=++++++++++++++++++++++++++++.      |
 |   .---------------------------=+++++++++++++++==---------=+++++++++++++++++++++++++++:       |
 |    .--------------------------=+++++++++++++++++==-------+++++++++++++++++++++++++++.        |
 |      ------------------------=+++++++++++++++++++++=----=++++++++++++++++++++++++++          |
 |       -----------------------=+++++++++++++++++++++++==-=++++++++++++++++++++++++=           |
 |        :---------------------++++++++++++++++++++++++++=++++++++++++++++++++++++-            |
 |         :-------------------=+++++++++++++++++++++++=====++++++++++++++++++++++-             |
 |          :------------------++++++++++++++++++++++=======+++++++++++++++++++++:              |
 |           .----------------=+++++++++++++++++++===========+++++++++++++++++++.               |
 |            .---------------++++++++++++++++++==============+++++++++++++++++.                |
 |              -------------=++++++++++++++++================+++++++++++++++=                  |
 |               ------------++++++++++++++====================+++++++++++++=                   |
 |                :---------=++++++++++++=======================+++++++++++-                    |
 |                 :--------=+++++++++==========================++++++++++:                     |
 |                  .------=++++++++=============================++++++++:                      |
 |                   .-----=+++++=================================++++++.                       |
 |                     ---=++++====================================++++.                        |
 |                      --=+=======================================++=                          |
 |                       :=------------------------------------------                           |
 |   Emerald Plus Microservice Command Tool                                                     |
 |   www.emerald.plus                                                                           |
 +----------------------------------------------------------------------------------------------+
 |   ./app.sh run all                                                                           |
 |   ./app.sh run integration                                                                   |
 |   ./app.sh run service component_a_command                                                   |
 |   ./app.sh run service component_a_command test                                              |
 |   ./app.sh run service component_a_command lint                                              |
 |                                                                                              |
 |   ./app.sh run local install                                                                 |
 |   ./app.sh run local --snapshot-update                                                       |
 |   ./app.sh run grpc_tools                                                                    |
 |                                                                                              |
 |   ./app.sh exec component_a_command                                                          |
 |   ./app.sh restart component_a_command                                                       |
 |                                                                                              |
 |   ./app.sh kill all                                                                          |
 |                                                                                              |
 |   ./app.sh delete all                                                                        |
 +----------------------------------------------------------------------------------------------+
```

### Description 

Emerald Plus Microservice is an open-source architecture template that implements CQRS Architecture using Django GRPS Framework, Kafka, Redis and MySQL.

### How to use it?

It is very simple. The template provides simple shell-script that helps developers to navigate the microservice.

1. `chmod +x app.sh`
2. `./app.sh run local install` - will install dependencies for local development
3. `./app.sh run all` - will run all docker container services
3. `./app.sh run integration` - will run all tests in service
4. `./app.sh run grpc_tools` - will run grpc_tools to generate libraries based on the protoc structure


### Project details
Project file structure:
```
- app
    |
    +- component_a              // components in the project
    |   |
    |   +- command              // Create | Update | Destroy
    |   |   |
    |   |   +- handlers.py      // Kafka Handlers
    |   |   
    |   |
    |   +- common
    |   |
    |   +- query                // List | Retrieve 
    |       |
    |       +- handlers.py      // GRPC Handlers
    |
    |
    +- integration_tests
    |   |
    |   +- component_a
    |
    |
    +- shared
        |
        +- library
        |   |
        |   +- component_a      // generated by grpc tools
        |
        +- protoc
            |
            +- component_a

- app.env                       // ENV variables
- app.sh
- docker-compose.yaml           // docker services
```

### Template Example
The template contains simple example of using `shared/protoc/command/person.proto`, `shared/protoc/common/person_message.proto` and `shared/protoc/query/person.proto`, that implements the coding standard, of splitting the `read` from the `write` services.
Also, `app/component_a` contains sample implementation of command services and query services.

### IMPORTANT
To test the Kafka Events you can create simple script, the messages should be configured as the following example.
```python
import os
from kafka import KafkaProducer
from shared.library.component_a.common import person_message_pb2

person_message = person_message_pb2.Person(query='Test command request', page_number=1, result_per_page=1)

producer = KafkaProducer(bootstrap_servers=os.environ.get('BOOTSTRAP_SERVERS'))
producer.send(topic=os.environ.get('SERVICE_TOPIC'), key=b'PersonController.Create:Person',
              value=bytes(person_message.SerializeToString()))
```

For more information feel free to contact me: mitko.mirevsky@gmail.com
