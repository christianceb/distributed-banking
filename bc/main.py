import logging
import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)

def runBumpSync():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        
        response: helloworld_pb2.BumpResponse = stub.Bump(helloworld_pb2.BumpRequest(count=5));

        flattenedStringedIntegers = [str(bump.timestamp) for bump in response.result]
        # flattenedIntegers = [ts for bump in response.result for ts in bump.timestamp]

        print("Bump client received: " + ", ".join(flattenedStringedIntegers))

if __name__ == "__main__":
    logging.basicConfig()
    
    # run()
    
    runBumpSync()
