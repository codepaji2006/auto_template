#include <iostream>
#include <cstring>
using namespace std;
template<class T> class X{
	private:
		T _privT;
	public:
		X(T v):_privT(v){}
		X();
		T getVal();
		void setVal(T v);
};


