#!/bin/sh

python -m grpc_tools.protoc \
    -I ./protos \
    --python_out=./shared \
    --pyi_out=./shared \
    --grpc_python_out=./shared \
    ./protos/helloworld.proto
