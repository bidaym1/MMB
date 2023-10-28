#include "callbacks.h"
#include "dish.h"
#include <array>
#include <iostream>

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

cbPDESigma Exporter::getPDE(int layer){
    double **p = dish->PDEfield->SigmaPointer(layer);  
    double *q = p[0];
    return cbPDESigma(par.sizey, par.sizex, q);
}

void Exporter::setCallback(Callback* callback)
{
    dish->CPM->setCallback(callback);
}
