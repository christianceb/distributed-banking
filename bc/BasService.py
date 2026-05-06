from grpc import Channel
import grpc


class BasService:
    channel: Channel
    connectionString: str

    def __init__(self, basConnectionString: str):
        self.connectionString = basConnectionString
        self.channel = grpc.insecure_channel('localhost:50051')

    def login(self, username: str , password: str):
        with self.channel:
            # TODO Put in login

            # Basic example
            # stub = helloworld_pb2_grpc.GreeterStub(channel)
            # response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            pass
    
    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
