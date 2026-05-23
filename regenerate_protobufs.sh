#!/bin/sh

# grpc_generated

python -m grpc_tools.protoc \
    -I grpc_generated=protos \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    ./protos/BankingApp.proto

python -m grpc_tools.protoc \
    -I grpc_generated=protos \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    ./protos/InternalBanking.proto
