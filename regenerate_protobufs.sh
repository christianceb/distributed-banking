#!/bin/sh

# Regenerate for shared

# python -m grpc_tools.protoc \
#     -I ./protos \
#     --python_out=./shared \
#     --pyi_out=./shared \
#     --grpc_python_out=./shared \
#     ./protos/helloworld.proto

# Regenerate for BC

python -m grpc_tools.protoc \
    -I ./protos \
    --python_out=./bc \
    --pyi_out=./bc \
    --grpc_python_out=./bc \
    ./protos/BankingApp.proto

# Regenerate for BAS

python -m grpc_tools.protoc \
    -I ./protos \
    --python_out=./bas \
    --pyi_out=./bas \
    --grpc_python_out=./bas \
    ./protos/BankingApp.proto

