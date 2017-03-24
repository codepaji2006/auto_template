#include "class_Y.h"
template<class T> Y<T>::Y(){
}
template<class T> T Y<T>::getVal(){
	return this->_privT;
}
template<class T> void Y<T>::setVal(T v){
	this->_privT=v;
}
