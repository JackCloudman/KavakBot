import json
from typing import Any, Dict, List

import typesense

from app.repositories.car_catalog.car_catalog_repository_interface import \
    CarCatalogRepositoryInterface


class CarCatalogRepository(CarCatalogRepositoryInterface):
    def __init__(self, typesense_client: typesense.Client, collection_name: str) -> None:
        self.client: typesense.Client = typesense_client
        self.collection_name: str = collection_name

    def search(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Método de búsqueda con manejo de excepciones para JSON inválido.
        """
        try:
            query: Dict[str, Any] = json.loads(search_query)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON query: {e}")
            return []

        filter_conditions: List[str] = []
        full_text_query: str = ""

        for column, condition in query.items():
            # Si detectamos el campo 'description', lo tratamos como búsqueda de texto completo
            if column == "description":
                if isinstance(condition, str) and condition.strip():
                    full_text_query = condition
                continue

            # Manejo de filtros para otros campos
            if isinstance(condition, (int, float, bool, str)):
                if isinstance(condition, str):
                    filter_conditions.append(f"{column}:='{condition}'")
                else:
                    filter_conditions.append(f"{column}:={condition}")

            elif isinstance(condition, list):
                values: List[str] = []
                for val in condition:
                    if isinstance(val, str):
                        values.append(f"'{val}'")
                    else:
                        values.append(str(val))
                values_str: str = "[" + ",".join(values) + "]"
                filter_conditions.append(f"{column}:{values_str}")

            elif isinstance(condition, dict):
                for op, val in condition.items():
                    if op == "eq":
                        if isinstance(val, str):
                            filter_conditions.append(f"{column}:='{val}'")
                        else:
                            filter_conditions.append(f"{column}:={val}")
                    elif op == "gt":
                        filter_conditions.append(f"{column}:>{val}")
                    elif op == "gte":
                        filter_conditions.append(f"{column}:>={val}")
                    elif op == "lt":
                        filter_conditions.append(f"{column}:<{val}")
                    elif op == "lte":
                        filter_conditions.append(f"{column}:<={val}")

        filter_by: str = " && ".join(
            filter_conditions) if filter_conditions else ""
        q_value: str = full_text_query if full_text_query else "*"

        search_parameters: Dict[str, Any] = {
            "q": q_value,
            "query_by": "description",  # campos utilizados para búsqueda de texto
            "filter_by": filter_by,
            "per_page": 10
        }

        print("SEARCH PARAMS", search_parameters)
        try:
            results: Dict[str, Any] = self.client.collections[self.collection_name].documents.search(
                search_parameters)
            print("RESULTS", results)
        except Exception as e:
            print(f"Error searching in Typesense: {e}")
            return []

        if 'hits' in results:
            return [hit['document'] for hit in results['hits']]
        else:
            return []

    def get_unique_values(self, column: str) -> List[Any]:
        """
        To get unique values from a particular column in Typesense, we can use facets.
        Make sure that the column is set as a facet field in the schema.
        """
        search_parameters: Dict[str, Any] = {
            "q": "*",
            "query_by": "description",  # or other text field used for full-text search
            "facet_by": column,
            "max_facet_values": 5000,
            "per_page": 0
        }

        results: Dict[str, Any] = self.client.collections[self.collection_name].documents.search(
            search_parameters)

        unique_values: List[Any] = []
        if 'facets' in results:
            for facet in results['facets']:
                if facet['field_name'] == column:
                    for val_count in facet['counts']:
                        unique_values.append(val_count['value'])
        return unique_values

    def get_columns(self) -> List[str]:
        """
        Retrieve the list of fields from the collection schema.
        """
        collection: Dict[str,
                         Any] = self.client.collections[self.collection_name].retrieve()
        fields: List[Dict[str, Any]] = collection.get('fields', [])
        return [f['name'] for f in fields]
