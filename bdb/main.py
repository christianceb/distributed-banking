import logging
from bdb.Backend import Backend


def app():
    Backend()

if __name__ == "__main__":
    logging.basicConfig()

    app()
