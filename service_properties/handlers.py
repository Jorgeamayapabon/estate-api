import json
import logging
from http.server import BaseHTTPRequestHandler

from service_properties.filters import parse_filters
from service_properties.service import list_properties

logger = logging.getLogger(__name__)


class PropertyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/properties":
            self._respond(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            self._respond(400, {"error": "Invalid JSON body"})
            return

        try:
            filters = parse_filters(body)
        except ValueError as exc:
            self._respond(400, {"error": str(exc)})
            return

        try:
            properties = list_properties(filters)
            self._respond(200, properties)
        except Exception:
            logger.exception("Unhandled error in list_properties")
            self._respond(500, {"error": "Internal server error"})

    def _respond(self, status: int, data) -> None:
        payload = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        logger.info("%s - %s", self.address_string(), fmt % args)
