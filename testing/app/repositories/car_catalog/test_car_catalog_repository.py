import json
from unittest.mock import MagicMock

import pytest

from app.repositories.car_catalog.car_catalog_repository import \
    CarCatalogRepository


class TestCarCatalogRepository:

    @pytest.fixture
    def typesense_client(self):
        return MagicMock()

    @pytest.fixture
    def repository(self, typesense_client):
        return CarCatalogRepository(typesense_client, "cars")

    def test_search(self, repository, typesense_client):
        search_query = json.dumps({
            "make": "chevrolet",
            "year": {"gte": 2018, "lte": 2020},
            "price": {"lte": 200000},
            "car_play": True,
            "description": "family car"
        })
        expected_results = {
            "hits": [
                {"document": {"make": "chevrolet", "year": 2019, "price": 150000, "car_play": True,
                              "description": "family car"}}
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        results = repository.search(search_query)

        assert results == [expected_results["hits"][0]["document"]]

    def test_get_unique_values(self, repository, typesense_client):
        column = "make"
        expected_results = {
            "facets": [
                {
                    "field_name": "make",
                    "counts": [{"value": "chevrolet"}, {"value": "ford"}]
                }
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        unique_values = repository.get_unique_values(column)

        assert unique_values == ["chevrolet", "ford"]

    def test_get_columns(self, repository, typesense_client):
        expected_schema = {
            "fields": [
                {"name": "make"},
                {"name": "year"},
                {"name": "price"},
                {"name": "car_play"},
                {"name": "description"}
            ]
        }
        typesense_client.collections["cars"].retrieve.return_value = expected_schema

        columns = repository.get_columns()

        assert columns == ["make", "year", "price", "car_play", "description"]
