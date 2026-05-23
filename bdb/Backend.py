import grpc
from concurrent import futures
from bdb.GrpcBackend import GrpcBackend
from grpc import Channel, Server
from grpc_generated.InternalBanking_pb2_grpc import add_InternalBankingServicer_to_server
from bdb.dependencies import database
from bdb.worker import worker_job


class UtilityInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)

        if handler is None:
            return None

        if handler.unary_unary:
            original = handler.unary_unary

            def wrapped(request, context):
                self.before_hook()

                result = original(request, context)

                self.after_hook()

                return result

            return grpc.unary_unary_rpc_method_handler(
                wrapped,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler
    
    def before_hook(self):
        try:
            connection = database()
            worker_job(connection)
        except Exception as e:
            connection.close()
            raise e
        finally:
            connection.close()

    def after_hook(self):
        pass
        # print("After Hook")

class Backend:
    port = "50061"
    server: Server
    
    channel: Channel
    connection_string: str

    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), interceptors=[UtilityInterceptor()])

        add_InternalBankingServicer_to_server(
            GrpcBackend(),
            self.server
        )

        self.server.add_insecure_port("0.0.0.0:" + self.port)
        
        self.server.start()
        
        print("BDB Server started, listening on " + self.port)
        
        self.server.wait_for_termination()
