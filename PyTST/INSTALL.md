Install the Python C Foreign Function Interface: 
pip install cffi

To build the shared library, run:
cd libTST/build
qmake ../libTST.pro
make
make install
