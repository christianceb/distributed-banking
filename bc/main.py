import logging
from BasService import BasService
from CliApplication import CliApplication


def app():
    CliApplication(BasService("localhost:50051"))

if __name__ == "__main__":
    # Maybe keep this gRPC demo artifact for now (might be useful later)
    logging.basicConfig()

    app()
