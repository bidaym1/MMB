#include "callbacks.h"
#include "dish.h"
#include <array>
#include <iostream>
#include <pybind11/numpy.h>

const int colortable[256][3] = {
#include "default.txt"
};

void Dish::Init()
{
    CPM->GrowInCells(par.n_init_cells, par.size_init_cells, par.subfield);
    CPM->ConstructInitCells(*this);
    for (int i = 0; i < par.divisions; i++)
        CPM->DivideCells();

    CPM->SetRandomTypes();
    std::cout << "Setting init callback" << std::endl;
    CPM->getCallback()->callback_init({ par.sizey, par.sizex, CPM->GetSigmaPtr()[0] });
    std::cout << "Set init callback" << std::endl;

    setTargetArea();
}

int PDE::MapColour(double val)
{
    return 0;
}

class Exporter {
private:
    Dish* dish;

public:
    Exporter(const std::string&);
    ~Exporter();
    void timestep();
    int getSigmaAt(const int, const int);
    cbSigma getSigma();
    void setCallback(Callback*);
    int getNumOfCells() { return dish->CountCells(); }
    int getColorOfCell(int cell)
    {
        return dish->CPM->getCell(cell).Colour();
    }
    void dishInit()
    {
        dish->Init();
    }
    int copy_prob(double DH, double stiff)
    {
        return dish->CPM->CopyvProb(DH, stiff);
    }
    cbPDESigma getPDE(int layer);
    void computeDrawing(pybind11::array_t<int> drawing, int border_color);
    //pybind11::array_t<int> computeDrawing(pybind11::array_t<int> drawing, int border_color);
};

Exporter::Exporter(const std::string& filename)
{
    std::cout << "Running exporter constructor" << std::endl;
    par.Read(filename.c_str());
    std::cout << "Done reading.." << std::endl;
    Seed(par.rseed);
    dish = new Dish;
    std::cout << "Done with: Running exporter constructor" << std::endl;
};
Exporter::~Exporter()
{
    std::cout << "Exporter is getting deleted!!" << std::endl;
    delete dish;
}
void Exporter::timestep()
{
    static int i = 0;
    dish->CPM->AmoebaeMove(dish->PDEfield);
    dish->CPM->getCallback()->callback_timestep({ par.sizey, par.sizex, dish->CPM->GetSigmaPtr()[0] });
    i++;
}
int Exporter::getSigmaAt(const int x, const int y)
{
    return dish->CPM->Sigma(x, y);
}
cbSigma Exporter::getSigma()
{
    int** p = dish->CPM->GetSigmaPtr();
    int* q = p[0];
    return cbSigma(par.sizey, par.sizex, q);
}

cbPDESigma Exporter::getPDE(int layer)
{
    double** p = dish->PDEfield->SigmaPointer(layer);
    double* q = p[0];
    return cbPDESigma(par.sizey, par.sizex, q);
}

void Exporter::setCallback(Callback* callback)
{
    dish->CPM->setCallback(callback);
}

//pybind11::array_t<int> Exporter::computeDrawing(pybind11::array_t<int> drawing, int border_color)
void Exporter::computeDrawing(pybind11::array_t<int> drawing, int border_color)
{
    pybind11::buffer_info drawing_info = drawing.request();
    auto drawing_ptr = static_cast<int*>(drawing_info.ptr);

    cout << "shape = ";
    for (auto shape : drawing_info.shape)
        cout << shape << ',';
    cout << endl;

    for (int i = 0; i < par.sizex; i++) {
        for (int j = 0; j < par.sizey; j++) {
            int spin = getSigmaAt(i, j);
            int type = dish->CPM->getCell(spin).getTau();
            int R = colortable[type][0];
            int G = colortable[type][1];
            int B = colortable[type][2];

            cout << i << ' ' << j << " R: " << drawing_ptr[i * drawing_info.shape[1]*drawing_info.shape[0] + j * drawing_info.shape[0]] << endl;
            cout << i << ' ' << j << " G: " << drawing_ptr[i * drawing_info.shape[1]*drawing_info.shape[0] + j * drawing_info.shape[0]+1] << endl;
            cout << i << ' ' << j << " B: " << drawing_ptr[i * drawing_info.shape[1]*drawing_info.shape[0] + j * drawing_info.shape[0]+2] << endl;

            drawing_ptr[i * drawing_info.shape[1]*drawing_info.shape[0] + j * drawing_info.shape[0]] = R;
            drawing_ptr[i * drawing_info.shape[1]*drawing_info.shape[0] + j * drawing_info.shape[0] + 1] = G;
            drawing_ptr[i * drawing_info.shape[1]*drawing_info.shape[0] + j * drawing_info.shape[0] + 2] = B;

        }
    }
    //return drawing;
}

//            if (spin > 0) {
//                int R = colortable[border_color][0];
//                int G = colortable[border_color][1];
//                int B = colortable[border_color][2];
//                if (i + 1 < par.sizey) {
//                    int next_spin = getSigmaAt(i + 1, j);
//                    if (spin != next_spin) {
//                        drawing_ptr[(i + 1) * drawing_info.shape[0] + j * drawing_info.shape[1]] = R;
//                        drawing_ptr[(i + 1) * drawing_info.shape[0] + j * drawing_info.shape[1] + 1] = G;
//                        drawing_ptr[(i + 1) * drawing_info.shape[0] + j * drawing_info.shape[1] + 2] = B;
//
//                    }
//                }
//                if (j + 1 < par.sizex) {
//                    int next_spin = getSigmaAt(i, j+1);
//                    if (spin != next_spin) {
//                        drawing_ptr[i * drawing_info.shape[0] + (j+1) * drawing_info.shape[1]] = R;
//                        drawing_ptr[i * drawing_info.shape[0] + (j+1) * drawing_info.shape[1] + 1] = G;
//                        drawing_ptr[i * drawing_info.shape[0] + (j+1) * drawing_info.shape[1] + 2] = B;
//                    }
//                }
//            }
//        }
//    }
//}
