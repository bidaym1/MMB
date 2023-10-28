#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
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
PYBIND11_MODULE(module, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
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
