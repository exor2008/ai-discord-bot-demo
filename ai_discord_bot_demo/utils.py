import logging
import os
import threading
from http import server

from dotenv import load_dotenv

load_dotenv()


def listen_http() -> None:
    """
    Start dummy http server to trick Google Cloud Run
    """

    def _listen_http() -> None:
        s = server.HTTPServer(("", 8080), server.SimpleHTTPRequestHandler)
        logger.info("Listening for 127.0.0.1:8080...")
        s.serve_forever()

    p = threading.Thread(target=_listen_http)
    p.start()


logger = logging.getLogger("AIbot logger")
logger.setLevel(os.environ["LOG_LEVEL"])
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
