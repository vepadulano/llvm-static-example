#!/bin/bash

set -ex

# Create build directory
mkdir -p build
cd build

# Configure with CMake
cmake ${CMAKE_ARGS} \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DCMAKE_PREFIX_PATH=$PREFIX \
    -DLLVM_DIR=$PREFIX/lib/cmake/llvm \
    -DBUILD_SHARED_LIBS=OFF \
    $SRC_DIR

# Build
make -j${CPU_COUNT}

# Install
make install
