import unittest
from unittest.mock import MagicMock, patch

from service_properties.repository import get_properties


def _make_conn_mock(rows):
    """Return a mock connection whose cursor yields the given rows."""
    cur = MagicMock()
    cur.fetchall.return_value = rows
    conn = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur


class TestGetProperties(unittest.TestCase):

    @patch("service_properties.repository.get_connection")
    def test_no_filters_executes_base_query(self, mock_conn_fn):
        conn, cur = _make_conn_mock([])
        mock_conn_fn.return_value = conn

        get_properties({})

        query, params = cur.execute.call_args.args
        self.assertIn("s.name IN ('pre_venta', 'en_venta', 'vendido')", query)
        self.assertEqual(params, [])

    @patch("service_properties.repository.get_connection")
    def test_year_filter_adds_clause_and_param(self, mock_conn_fn):
        conn, cur = _make_conn_mock([])
        mock_conn_fn.return_value = conn

        get_properties({"year": 2018})

        query, params = cur.execute.call_args.args
        self.assertIn("p.year = %s", query)
        self.assertIn(2018, params)

    @patch("service_properties.repository.get_connection")
    def test_city_filter_uses_lowercase_comparison(self, mock_conn_fn):
        conn, cur = _make_conn_mock([])
        mock_conn_fn.return_value = conn

        get_properties({"city": "bogota"})

        query, params = cur.execute.call_args.args
        self.assertIn("LOWER(p.city) = %s", query)
        self.assertIn("bogota", params)

    @patch("service_properties.repository.get_connection")
    def test_status_filter_adds_clause_and_param(self, mock_conn_fn):
        conn, cur = _make_conn_mock([])
        mock_conn_fn.return_value = conn

        get_properties({"status": "en_venta"})

        query, params = cur.execute.call_args.args
        self.assertIn("s.name = %s", query)
        self.assertIn("en_venta", params)

    @patch("service_properties.repository.get_connection")
    def test_combined_filters_add_all_clauses(self, mock_conn_fn):
        conn, cur = _make_conn_mock([])
        mock_conn_fn.return_value = conn

        get_properties({"year": 2000, "city": "medellin", "status": "vendido"})

        query, params = cur.execute.call_args.args
        self.assertIn("p.year = %s", query)
        self.assertIn("LOWER(p.city) = %s", query)
        self.assertIn("s.name = %s", query)
        self.assertEqual(len(params), 3)

    @patch("service_properties.repository.get_connection")
    def test_returns_cursor_rows(self, mock_conn_fn):
        rows = [{"address": "calle 1", "city": "bogota", "status": "en_venta",
                 "price": 100000000, "description": "desc"}]
        conn, _ = _make_conn_mock(rows)
        mock_conn_fn.return_value = conn

        result = get_properties({})
        self.assertEqual(result, rows)

    @patch("service_properties.repository.get_connection")
    def test_connection_is_always_closed(self, mock_conn_fn):
        conn, cur = _make_conn_mock([])
        mock_conn_fn.return_value = conn

        get_properties({})

        conn.close.assert_called_once()
        cur.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
