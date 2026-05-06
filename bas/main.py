import logging
from Backend import Backend


def app():
    Backend()

if __name__ == "__main__":
    logging.basicConfig()

    app()
