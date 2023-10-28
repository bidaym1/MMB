#!/bin/bash
git submodule init
git submodule update
mv pybind11 libTST
rm -r libTST/build
mkdir libTST/build
cd libTST/build

cmake ..
make -j 8

mv module* ../../PyTSTv2

