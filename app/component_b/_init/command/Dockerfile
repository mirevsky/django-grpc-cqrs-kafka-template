FROM python:3.8
ARG bootstrap_servers
ENV BOOTSTRAP_SERVERS "${bootstrap_servers}"
ARG service_topic
ENV SERVICE_TOPIC "${service_topic}"
ARG user

ENV PYTHONPATH="${PYTHONPATH}:/shared"

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./shared /shared
COPY ./requirements.txt /requirements.txt
COPY ./component_b /component_b

RUN pip install -r /requirements.txt

CMD /component_b/shell/run_it.sh run command_controller