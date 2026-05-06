import logging
from bc import CliApplication


def app():
    CliApplication(BasService())

if __name__ == "__main__":
    # Maybe keep this gRPC demo artifact for now (might be useful later)
    logging.basicConfig()

    app()
