import grpc
import sqlite3
from concurrent import futures
from GrpcBackend import GrpcBackend
from grpc import Channel, Server
from InternalBanking_pb2_grpc import add_InternalBankingServicer_to_server


class Backend:
    port = "50061"
    server: Server
    
    channel: Channel
    connection_string: str

    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

        add_InternalBankingServicer_to_server(
            GrpcBackend(),
            self.server
        )

        self.server.add_insecure_port("[::]:" + self.port)
        
        self.server.start()
        
        print("BDB Server started, listening on " + self.port)
        
        self.server.wait_for_termination()
