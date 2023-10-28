#pragma once
#include <functional>
#include <iostream>

// TODO: make a template class so we can use different datatypes. Except ints and doubles
class cbPDESigma {
public:
    cbPDESigma(int rows, int cols) : m_rows(rows), m_cols(cols) {
        m_data = new double[rows*cols];
    }
    cbPDESigma(int rows, int cols, double* p) : m_rows(rows), m_cols(cols) {
        m_data = p;
    }
    double *data() { return m_data; }
    int rows() const { return m_rows; }
    int cols() const { return m_cols; }
private:
    int m_rows, m_cols;
    double *m_data;
};
class cbSigma {
public:
    cbSigma(int rows, int cols) : m_rows(rows), m_cols(cols) {
        m_data = new int[rows*cols];
    }
    cbSigma(int rows, int cols, int* p) : m_rows(rows), m_cols(cols) {
        m_data = p;
    }
    int *data() { return m_data; }
    int rows() const { return m_rows; }
    int cols() const { return m_cols; }
private:
    int m_rows, m_cols;
    int *m_data;
};

typedef std::function<int(cbSigma,int,int,int,int,int,int)> type_cb_copy_attempt;
typedef std::function<void(cbSigma)> type_cb_init;
typedef std::function<void(cbSigma)> type_cb_timestep;
//typedef std::function<int(int,double)> type_cb_copy_prob;
class Callback
{
	public:
		type_cb_copy_attempt callback_copy_attempt;
		type_cb_init callback_init;
		type_cb_timestep callback_timestep;
	//	type_cb_copy_prob callback_copy_prob;
		Callback(){}
		~Callback(){std::cout << "Callback destroyed" << std::endl;}
		void set_copyattempt(const type_cb_copy_attempt &f) {
			callback_copy_attempt = f;
		}
		void set_init(const type_cb_init &f) {
			callback_init = f;
		}
		void set_timestep(const type_cb_timestep &f){
			callback_timestep = f;
		}
		//void set_copy_prob(const type_cb_copy_prob &f){
		//	callback_copy_prob = f;
		//}
};
