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

python -m grpc_tools.protoc \
    -I ./protos \
    --python_out=./bas \
    --pyi_out=./bas \
    --grpc_python_out=./bas \
    ./protos/InternalBanking.proto


# Regenerate for BDB

python -m grpc_tools.protoc \
    -I ./protos \
    --python_out=./bdb \
    --pyi_out=./bdb \
    --grpc_python_out=./bdb \
    ./protos/InternalBanking.proto

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
