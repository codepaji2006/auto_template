#include <iostream>
#include <string>
#include "X/class_X.h"
#include "Y/class_Y.h"
using namespace std;

int main()
{

	X<int> *instof_X=new X<int>();
	instof_X->setVal(100);
	cout<<"x_v(int)="<<instof_X->getVal()<<"\n";
	delete(instof_X);

	X<float> *finstof_X=new X<float>();
	finstof_X->setVal(0.324324);
	cout<<"x_v(float)="<<finstof_X->getVal()<<"\n";
	delete(finstof_X);

	Y<char> *cinstof_Y=new Y<char>();
	cinstof_Y->setVal('a');
	cout<<"y_v(char)="<<cinstof_Y->getVal()<<"\n";
	delete(cinstof_Y);
	return 0;
}
