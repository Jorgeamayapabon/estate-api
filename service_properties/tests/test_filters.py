import unittest

from service_properties.filters import parse_filters


class TestParseFilters(unittest.TestCase):

    # --- happy path ---

    def test_empty_body_returns_empty_filters(self):
        self.assertEqual(parse_filters({}), {})

    def test_valid_year(self):
        result = parse_filters({"year": 2020})
        self.assertEqual(result["year"], 2020)

    def test_valid_city_is_lowercased(self):
        result = parse_filters({"city": "Bogota"})
        self.assertEqual(result["city"], "bogota")

    def test_valid_city_strips_whitespace(self):
        result = parse_filters({"city": "  medellin  "})
        self.assertEqual(result["city"], "medellin")

    def test_valid_status_pre_venta(self):
        result = parse_filters({"status": "pre_venta"})
        self.assertEqual(result["status"], "pre_venta")

    def test_valid_status_en_venta(self):
        result = parse_filters({"status": "en_venta"})
        self.assertEqual(result["status"], "en_venta")

    def test_valid_status_vendido(self):
        result = parse_filters({"status": "vendido"})
        self.assertEqual(result["status"], "vendido")

    def test_all_filters_combined(self):
        result = parse_filters({"year": 2018, "city": "Cali", "status": "en_venta"})
        self.assertEqual(result, {"year": 2018, "city": "cali", "status": "en_venta"})

    def test_unknown_keys_are_ignored(self):
        result = parse_filters({"unknown_key": "value", "year": 2010})
        self.assertNotIn("unknown_key", result)
        self.assertEqual(result["year"], 2010)

    # --- year validation ---

    def test_year_as_string_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"year": "2020"})

    def test_year_as_float_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"year": 2020.0})

    def test_year_as_bool_raises(self):
        # bool is subclass of int in Python — must be rejected explicitly
        with self.assertRaises(ValueError):
            parse_filters({"year": True})

    # --- city validation ---

    def test_empty_city_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"city": ""})

    def test_whitespace_only_city_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"city": "   "})

    def test_non_string_city_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"city": 123})

    # --- status validation ---

    def test_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"status": "comprando"})

    def test_internal_status_comprado_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"status": "comprado"})

    def test_empty_status_raises(self):
        with self.assertRaises(ValueError):
            parse_filters({"status": ""})


if __name__ == "__main__":
    unittest.main()
