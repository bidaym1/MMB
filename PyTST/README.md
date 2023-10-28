
Clone this repo with "git clone --recursive git@github.com:koen219/PyTST2.git"

If you did not clone this repo with the --recursive keyword you should run:

git submodule init
git submodule update

The following steps should automaticaly be done by the install.sh script.
Install with the following:

mv pybind11 libTST  
mkdir libTST/build  
cd libTST/build  
cmake ..   
make  

Next copy the just created module file in the build directory (name is platform dependend) to PyTSTv2. You can test it by running "python CPM2.py {PARAMETERFILE}".

Atleast the following packages are needed to let this all work:

PyQt5
pyqtgraph
numba
numpy

and possibly more.
