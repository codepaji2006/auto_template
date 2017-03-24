#include "class_X.h"
template<class T> X<T>::X(){
}
template<class T> T X<T>::getVal(){
	return this->_privT;
}
template<class T> void X<T>::setVal(T v){
	this->_privT=v;
}
