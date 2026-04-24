import logging
from http.server import HTTPServer

from service_properties.handlers import PropertyHandler

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

HOST = "0.0.0.0"
PORT = 8080

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), PropertyHandler)
    logging.info("Server running on http://%s:%d", HOST, PORT)
    server.serve_forever()
