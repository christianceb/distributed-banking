import logging
from bc.BasService import BasService
from bc.CliApplication import CliApplication


def app(bas_connection_string: str = "localhost:10051"):
    CliApplication(BasService(bas_connection_string))

if __name__ == "__main__":
    # Maybe keep this gRPC demo artifact for now (might be useful later)
    logging.basicConfig()

    app()
