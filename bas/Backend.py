import grpc

from concurrent import futures
from grpc import Channel, Server
from grpc_generated.BankingApp_pb2_grpc import add_BankingAppServicer_to_server
from bas.BankingDatabaseService import BankingDatabaseService
from bas.GrpcBackend import GrpcBackend
from bas.UserTokenService import UserTokenService


class Backend:
    port = "10051"
    server: Server
    
    channel: Channel
    connectionString: str

    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
        add_BankingAppServicer_to_server(
            GrpcBackend(
                BankingDatabaseService("localhost:10061"),
                UserTokenService()
            ),
            self.server
        )
        
        self.server.add_insecure_port("0.0.0.0:" + self.port)
        
        self.server.start()
        
        print("BAS Server started, listening on " + self.port)
        
        self.server.wait_for_termination()
