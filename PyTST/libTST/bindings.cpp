#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "exporter.h"
#include "callbacks.h"
#include <iostream>
/*
int main(){
	Dish *dish = new Dish();
	std::cout << "This runs" << std::endl;
	return 0;
}
*/


int func_arg(const std::function<int(int)> &f){
	return f(10);
}
namespace py = pybind11;


//// Passing in an array of doubles
//void computeDrawing(
//        py::array_t<int> sigma,
//        py::array_t<int> drawing,
//        py::array_t<int> types) {
//
//    /*
//     * sigma is a square field of say 200x200 and drawing is double that field sizex x sizey x 3
//     * the RGB values of cells are filled in based on the bases of the types.
//     * The array types indices every value to the types
//     */
//
//    py::buffer_info sigma_info = sigma.request();
//    auto sigma_ptr = static_cast<int *>(sigma_info.ptr);
//
//    for (int i=0; i<sigma_info.shape[0]; i++){
//        for (int j=0; j<sjgma_jnfo.shape[1]; j++) {
//            if (sigma_ptr[ sigma_info[0]*i + j] > 0){
//                
//            }
//        }
//    }
//
//    cout << "shape n " << n << endl;
//    cout << "3,4:" << endl;
//    cout << ptr[info.shape[1]*3+4] << endl;
//
//}

PYBIND11_MODULE(module, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    //m.def("computeDrawing", &computeDrawing, "Takes a sigma array and doubles it"); 
    py::class_<Exporter>(m, "Exporter")
        .def(py::init<const std::string &>())
        .def("timestep", &Exporter::timestep)
		.def("getSigma", &Exporter::getSigma)
		.def("setCallback", &Exporter::setCallback)
        .def("getColorOfCell", &Exporter::getColorOfCell)
        .def("dishInit", &Exporter::dishInit)
        .def("getNumOfCells", &Exporter::getNumOfCells)
        .def("copy_prob", &Exporter::copy_prob)
        .def("getPDE", &Exporter::getPDE)
        .def("SecreteAndDiffusePDE", &Exporter::SecreteAndDiffuse)
        .def("computeDrawing", &Exporter::computeDrawing)
        ;
	py::class_<Callback>(m, "Callback")
		.def(py::init<>())
		.def("set_copyattempt", &Callback::set_copyattempt)
		.def("set_init", &Callback::set_init)
		.def("set_timestep", &Callback::set_timestep)
		;
	py::class_<cbSigma>(m, "cbSigma", py::buffer_protocol())
    .def_buffer([](cbSigma &m) -> py::buffer_info {
        return py::buffer_info(
            m.data(),                               /* Pointer to buffer */
            sizeof(int),                          /* Size of one scalar */
            py::format_descriptor<int>::format(), /* Python struct-style format descriptor */
            2,                                      /* Number of dimensions */
            { m.rows(), m.cols() },                 /* Buffer dimensions */
            { sizeof(int) * m.cols(),             /* Strides (in bytes) for each index */
              sizeof(int) }
        );
    })
	.def(py::init<size_t,size_t>())
	;
	py::class_<cbPDESigma>(m, "cbPDESigma", py::buffer_protocol())
    .def_buffer([](cbPDESigma &m) -> py::buffer_info {
        return py::buffer_info(
            m.data(),                               /* Pointer to buffer */
            sizeof(double),                          /* Size of one scalar */
            py::format_descriptor<double>::format(), /* Python struct-style format descriptor */
            2,                                      /* Number of dimensions */
            { m.rows(), m.cols() },                 /* Buffer dimensions */
            { sizeof(double) * m.cols(),             /* Strides (in bytes) for each index */
              sizeof(double) }
        );
    })
	.def(py::init<size_t,size_t>())
	;
}
