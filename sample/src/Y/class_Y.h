#include <iostream>
#include <cstring>
using namespace std;
template<class T> class Y{
	private:
		T _privT;
	public:
		Y(T v):_privT(v){}
		Y();
		T getVal();
		void setVal(T v);
};


