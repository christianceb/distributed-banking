import logging
import time
import grpc
from concurrent import futures
import helloworld_pb2_grpc
import helloworld_pb2
from random import randrange


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    queried: list[int] = []

    def bumpbump(self):
        self.queried.append(time.time_ns())

    def SayHello(self, request: helloworld_pb2.HelloRequest, context):
        self.bumpbump()

        return helloworld_pb2.HelloReply(message=str(len(self.queried)) + " - Hello, %s!" % request.name)
    
    def SayHelloAgain(self, request: helloworld_pb2.HelloRequest, context):
        self.bumpbump()

        return helloworld_pb2.HelloReply(
            message=str(len(self.queried)) + " - " + f"Hello again, {request.name}!"
        )
    
    def Bump(self, request: helloworld_pb2.BumpRequest, context):
        for _ in range(request.count):
            time.sleep(randrange(1,3))
            self.bumpbump()

        result = [helloworld_pb2.Bump(timestamp=timestampNs) for timestampNs in self.queried]

        return helloworld_pb2.BumpResponse(result=result)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
