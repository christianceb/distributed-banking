import logging
from bc.BasService import BasService
from bc.CliApplication import CliApplication


def app():
    CliApplication(BasService("localhost:10051"))

if __name__ == "__main__":
    # Maybe keep this gRPC demo artifact for now (might be useful later)
    logging.basicConfig()

    app()
