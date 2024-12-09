import json
from unittest.mock import MagicMock, patch

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
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_search_no_description(self, repository, typesense_client):
        search_query = json.dumps({
            "make": "ford",
            "year": {"gt": 2015},
            "price": {"lt": 300000},
            "car_play": False
            # No 'description' field
        })
        expected_results = {
            "hits": [
                {"document": {"make": "ford", "year": 2017,
                              "price": 250000, "car_play": False}}
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        results = repository.search(search_query)

        assert results == [expected_results["hits"][0]["document"]]
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_search_exception_handling(self, repository, typesense_client):
        search_query = json.dumps({
            "make": "toyota",
            "description": "reliable"
        })
        typesense_client.collections["cars"].documents.search.side_effect = Exception(
            "Typesense error")

        results = repository.search(search_query)

        assert results == []
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_search_empty_results(self, repository, typesense_client):
        search_query = json.dumps({
            "make": "bmw",
            "year": {"gte": 2022},
            "description": "luxury"
        })
        expected_results = {"hits": []}
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        results = repository.search(search_query)

        assert results == []
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_search_multiple_conditions(self, repository, typesense_client):
        search_query = json.dumps({
            "make": ["chevrolet", "ford"],
            "year": {"gt": 2015, "lt": 2021},
            "price": {"gte": 100000, "lte": 300000},
            "car_play": True
        })
        expected_results = {
            "hits": [
                {"document": {"make": "ford", "year": 2018,
                              "price": 200000, "car_play": True}},
                {"document": {"make": "chevrolet", "year": 2019,
                              "price": 250000, "car_play": True}}
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        results = repository.search(search_query)

        expected_documents = [hit["document"]
                              for hit in expected_results["hits"]]
        assert results == expected_documents
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

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
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_get_unique_values_no_facets(self, repository, typesense_client):
        column = "color"
        expected_results = {
            "facets": []
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        unique_values = repository.get_unique_values(column)

        assert unique_values == []
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_get_unique_values_multiple_facets(self, repository, typesense_client):
        column = "make"
        expected_results = {
            "facets": [
                {
                    "field_name": "make",
                    "counts": [{"value": "chevrolet"}, {"value": "ford"}, {"value": "toyota"}]
                },
                {
                    "field_name": "color",
                    "counts": [{"value": "red"}, {"value": "blue"}]
                }
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        unique_values = repository.get_unique_values(column)

        assert unique_values == ["chevrolet", "ford", "toyota"]
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

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
        typesense_client.collections["cars"].retrieve.assert_called_once()

    def test_get_columns_empty_schema(self, repository, typesense_client):
        expected_schema = {
            "fields": []
        }
        typesense_client.collections["cars"].retrieve.return_value = expected_schema

        columns = repository.get_columns()

        assert columns == []
        typesense_client.collections["cars"].retrieve.assert_called_once()

    def test_get_columns_missing_fields_key(self, repository, typesense_client):
        expected_schema = {}
        typesense_client.collections["cars"].retrieve.return_value = expected_schema

        columns = repository.get_columns()

        assert columns == []
        typesense_client.collections["cars"].retrieve.assert_called_once()

    @patch('app.repositories.car_catalog.car_catalog_repository.json.loads')
    def test_search_invalid_json(self, mock_json_loads, repository, typesense_client):
        mock_json_loads.side_effect = json.JSONDecodeError(
            "Expecting value", "", 0)
        search_query = "invalid json"

        results = repository.search(search_query)

        assert results == []
        mock_json_loads.assert_called_once_with(search_query)
        typesense_client.collections["cars"].documents.search.assert_not_called(
        )

    def test_search_with_eq_operator(self, repository, typesense_client):
        search_query = json.dumps({
            "make": {"eq": "honda"},
            "year": {"eq": 2020},
            "description": "compact"
        })
        expected_results = {
            "hits": [
                {"document": {"make": "honda", "year": 2020, "price": 180000, "car_play": True,
                              "description": "compact car"}}
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        results = repository.search(search_query)

        assert results == [expected_results["hits"][0]["document"]]
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )

    def test_search_with_in_operator(self, repository, typesense_client):
        search_query = json.dumps({
            "make": ["honda", "toyota"],
            "description": "reliable"
        })
        expected_results = {
            "hits": [
                {"document": {"make": "honda", "year": 2021, "price": 200000, "car_play": True,
                              "description": "reliable car"}},
                {"document": {"make": "toyota", "year": 2022, "price": 220000, "car_play": True,
                              "description": "reliable car"}}
            ]
        }
        typesense_client.collections["cars"].documents.search.return_value = expected_results

        results = repository.search(search_query)

        expected_documents = [hit["document"]
                              for hit in expected_results["hits"]]
        assert results == expected_documents
        typesense_client.collections["cars"].documents.search.assert_called_once(
        )
