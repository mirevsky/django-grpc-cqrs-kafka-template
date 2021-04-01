FROM python:3.8
ENV PYTHONPATH="${PYTHONPATH}:/shared"

COPY ./shared /shared
COPY ./requirements.txt /requirements.txt
COPY ./component_* /component_*
COPY ./integration_tests /integration_tests

RUN pip install -r /requirements.txt

CMD pytest /component_a -v && pytest /integration_tests -v