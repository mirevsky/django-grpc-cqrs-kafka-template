import pytest
from component_b.common.tests.fixtures import *
from django_grpc_framework.test import RPCTestCase

from component_b.common.tests.fixtures import *
from component_b.query.services import PersonQueryService


@pytest.mark.django_db
class TestPersonQueryService(RPCTestCase):

    def test_list(self, mock_products, snapshot):
        assert True

    def test_retrieve(self, mock_products, snapshot):
        assert True
