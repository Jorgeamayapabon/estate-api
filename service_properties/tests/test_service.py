import unittest
from unittest.mock import patch

from service_properties.service import list_properties

_FAKE_PROPERTIES = [
    {
        "address": "calle 23 #45-67",
        "city": "bogota",
        "status": "en_venta",
        "price": 120000000,
        "description": "Apartamento en el centro",
    }
]


class TestListProperties(unittest.TestCase):

    @patch("service_properties.service.get_properties")
    def test_returns_repository_results(self, mock_get):
        mock_get.return_value = _FAKE_PROPERTIES
        result = list_properties({})
        self.assertEqual(result, _FAKE_PROPERTIES)

    @patch("service_properties.service.get_properties")
    def test_passes_filters_to_repository(self, mock_get):
        mock_get.return_value = []
        filters = {"city": "bogota", "status": "en_venta"}
        list_properties(filters)
        mock_get.assert_called_once_with(filters)

    @patch("service_properties.service.get_properties")
    def test_empty_result_returns_empty_list(self, mock_get):
        mock_get.return_value = []
        result = list_properties({"year": 1800})
        self.assertEqual(result, [])

    @patch("service_properties.service.get_properties")
    def test_empty_filters_passed_through(self, mock_get):
        mock_get.return_value = _FAKE_PROPERTIES
        list_properties({})
        mock_get.assert_called_once_with({})


if __name__ == "__main__":
    unittest.main()
