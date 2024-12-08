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
        Example of query:
        {
            "make": "chevrolet",              # direct equality
            "year": {"gte": 2018, "lte": 2020}, # range with gte/lte/gt/lt/eq
            "price": {"lte": 200000},         # simple comparison
            "car_play": True,                 # direct equality
            "description": "family car"       # full-text search in the description field
        }
        """

        query: Dict[str, Any] = json.loads(search_query)

        filter_conditions: List[str] = []
        full_text_query: str = ""

        for column, condition in query.items():
            # If we detect the 'description' field, treat it as full-text search
            if column == "description":
                if isinstance(condition, str) and condition.strip():
                    full_text_query = condition
                # Skip adding to filter conditions since this is a text search field
                continue

            # Handle filters for other fields
            if isinstance(condition, (int, float, bool, str)):
                # Direct equality
                if isinstance(condition, str):
                    filter_conditions.append(f"{column}:='{condition}'")
                else:
                    filter_conditions.append(f"{column}:={condition}")

            elif isinstance(condition, list):
                # IN condition
                values: List[str] = []
                for val in condition:
                    if isinstance(val, str):
                        values.append(f"'{val}'")
                    else:
                        values.append(str(val))
                values_str: str = "[" + ",".join(values) + "]"
                filter_conditions.append(f"{column}:{values_str}")

            elif isinstance(condition, dict):
                # Range or comparison operators
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

        # Adjust query_by according to fields indexed for full-text search
        search_parameters: Dict[str, Any] = {
            "q": q_value,
            "query_by": "description",  # set fields used for text search
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
