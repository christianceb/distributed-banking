from concurrent import futures
from BankingApp_pb2_grpc import add_BankingAppServicer_to_server
from GrpcBackend import GrpcBackend
from grpc import Channel, Server
from UserTokenService import UserTokenService
import grpc

from BankingDatabaseService import BankingDatabaseService


class Backend:
    port = "50051"
    server: Server
    
    channel: Channel
    connectionString: str

    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
        add_BankingAppServicer_to_server(
            GrpcBackend(
                BankingDatabaseService("localhost:50061"),
                UserTokenService()
            ),
            self.server
        )
        
        self.server.add_insecure_port("[::]:" + self.port)
        
        self.server.start()
        
        print("BAS Server started, listening on " + self.port)
        
        self.server.wait_for_termination()
