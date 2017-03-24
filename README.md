# auto_template
# Automatically creates template instantiation code for C++ templates

# What this program does?

When code is complicated and requires usage of the template class in various forms in different locations, adding explicit instantiation and tracking it is difficult and leads to bugs.This program automatically creates all the instantiation code and the programmer does not have to worry about linker issues and instantiation problems.

# C++ templates and issues and why we need this :

C++ templates are a great way of generalizing specific operations and avoiding massive code duplication. It also speeds up software development and makes software design and use case deployment much easier. For example, let's say you have a requirement to authenticate users and currently you are saving passwords  in md5 (128 bit) hash format for example, the "/etc/shadow" file in linux flavors.  A list of these username and password hashes will look like this:<br/>
user1:0b987a20750257b256c2488676042234<br/>
user2:7264579de7cd46af1be5ad959cdcbf55<br/>
<br/>
A real /etc/shadow looks like this:<br/>
linux$# cat /etc/shadow<br/>
meuser:$1$FrhsiYWH$zx5BDHi5JUFIFwwl9f4.D/:16905:0:99999:7:::<br/>
<br/>
 A MD5 object can be used here with you MyAuth class where currently your class is defined as follows:
class MyAuth{<br/>
<tab/>private:<br/>
    char username[144];<br/>
    char md5hash[32];<br/>
  public:<br/>
    MyAuth(char* u,char* m){<br/>
      strncpy(username,u,144);<br/>
      strncpy(md5hash,m,32);<br/>
    }<br/>
    /*.....other code */<br/>
}<br/>

If you want to use SHA-1 instead you would have to write another class for SHA-1. Instead using a template it becomes much easier.<br/>
<br/>
template <class T> class MyAuth{<br/>
    private:<br/>
        T  hash;<br/>
        char username[144];<br/>
    public:<br/>
        MyAuth(char* u,T *h){<br/>
          hash = *h;<br/>
          strncpy(username,u,144);<br/>
        }<br/>
}<br/>
And you can use as :<br/>
<br/>
HashObject *hobj=<some hash object>(password)<br/>
char username[]="me2017";<br/>
MyAuth<HashObject> *ma=new MyAuth<HashObject>(username,hobj);<br/>
<br/>
# Problem:

This is all fine and nice and C++ has given us a way to avoid code duplication and bloating and also save time and debugging efforts. But when you need to use your template classes in a lot of places in your main project and they are everywhere, you will need to group files and package them and in that scenario the linker will fail.

# Background:

First,let's brush up on the compile and link process concept. All C++ code files (not headers) are compiled into an intermediate object file(.o) . If this .o object file references functions or variables that are defined in another object file, then these references are marked as unresolved or with a "U" as shown below. It is only during link stage, the linker resolves all references to create a final executable.
<br/>
devuser@ubuntu-14:~/auto_template/sample$ make<br/>
rm -f ./src/Y/class_Y.o ./src/X/class_X.o ./src/main.o<br/>
rm -f bin/sample<br/>
rm -f<br/>
ctags -R<br/>
g++ -c -Wall -g src/Y/class_Y.cpp -o src/Y/class_Y.o<br/>
g++ -c -Wall -g src/X/class_X.cpp -o src/X/class_X.o<br/>
g++ -c -Wall -g src/main.cpp -o src/main.o<br/>
g++  ./src/Y/class_Y.o ./src/X/class_X.o ./src/main.o -o bin/sample<br/>
./src/main.o: In function `main':<br/>
/home/devuser/auto_template/sample/src/main.cpp:10: undefined reference to `X<int>::X()'<br/>
/home/devuser/auto_template/sample/src/main.cpp:11: undefined reference to `X<int>::setVal(int)'<br/>
/home/devuser/auto_template/sample/src/main.cpp:12: undefined reference to `X<int>::getVal()'<br/>
/home/devuser/auto_template/sample/src/main.cpp:15: undefined reference to `X<float>::X()'<br/>
/home/devuser/auto_template/sample/src/main.cpp:16: undefined reference to `X<float>::setVal(float)'<br/>
/home/devuser/auto_template/sample/src/main.cpp:17: undefined reference to `X<float>::getVal()'<br/>
/home/devuser/auto_template/sample/src/main.cpp:20: undefined reference to `Y<char>::Y()'<br/>
/home/devuser/auto_template/sample/src/main.cpp:21: undefined reference to `Y<char>::setVal(char)'<br/>
/home/devuser/auto_template/sample/src/main.cpp:22: undefined reference to `Y<char>::getVal()'<br/>
collect2: error: ld returned 1 exit status<br/>
make: *** [bin/sample] Error 1<br/>
devuser@ubuntu-14:~/auto_template/sample$<br/>
<br/>
I am using :<br/>
gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3)<br/>
GNU Make 3.81<br/>
GNU nm (GNU Binutils for Ubuntu) 2.24<br/>
<br/>
Looking at the .o files using nm in main.o which uses the template classes X and Y.<br/>
0000000000000000 T main<br/>
                 U _Unwind_Resume<br/>
00000000000001ab t __static_initialization_and_destruction_0(int, int)<br/>
                 U operator delete(void*)<br/>
                 U X<float>::getVal()<br/>
                 U X<float>::setVal(float)<br/>
                 U X<float>::X()<br/>
                 U X<int>::getVal()<br/>
                 U X<int>::setVal(int)<br/>
                 U X<int>::X()<br/>
                 U Y<char>::getVal()<br/>
                 U Y<char>::setVal(char)<br/>
                 U Y<char>::Y()<br/>
                 U std::ostream::operator<<(float)<br/>
                 U std::ostream::operator<<(int)<br/>
                 U std::ios_base::Init::Init()<br/>
                 U std::ios_base::Init::~Init()<br/>
                 U operator new(unsigned long)<br/>
                 U std::cout<br/>
0000000000000000 b std::__ioinit<br/>
<br/>
Notice the U which is undefined so the error.<br/>
<br/>
You could declare your classes in a header file and link and it would solve this but it comes with its own issues.Programmers often complain when their templates have to entirely defined in a header file which causes unnecessary code duplication and excessive rebuilds anytime a single variable is changed in the class definitions.<br/>
<br/>
# The Solution:<br/>
<br/>
The solution to this problem and doing it elegantly is to explicitly declare instants of used <class T> usages in .cpp files so that during compile stage references to these instances are stored in .o files.This helps the linker to copy the address of this instance to the main executable.
So in a file "class_X_def.cpp",<br/>
#include "class_X.cpp"<br/>
template X<int>;<br/>
<br/>
This is called as "explicit instantiation". Refer draft C++  on isocpp.org website.<br/>
<br/>
# Usage of program:<br/>
<br/>
devuser@ubuntu-14:~/auto_template$ python auto_explicit_template_instantiation.py<br/>
Definition files:['./sample/src/Y/class_Y.h', './sample/src/X/class_X.h', './sample/src/Y/class_Y.cpp', './sample/src/X/class_X.cpp']<br/>
for class:Y {<br/>
                defined in directory:./sample/src/Y<br/>
                referred in files:['./sample/src/main.cpp']<br/>
                instances:{'./sample/src/main.cpp': ['char']}<br/>
}<br/>
def file name:./sample/src/Y/class_Y_def.cpp<br/>
#include "class_Y.cpp"<br/>
template class Y<char>;<br/>
<br/>
for class:X {<br/>
                defined in directory:./sample/src/X<br/>
               referred in files:['./sample/src/main.cpp']<br/>
                instances:{'./sample/src/main.cpp': ['int', 'float']<br/>
}<br/>

def file name:./sample/src/X/class_X_def.cpp<br/>
#include "class_X.cpp"<br/>
template class X<int>;<br/>

template class X<int>;<br/>
template class X<float>;<br/>

now if you compile:<br/>
<br/>
devuser@ubuntu-14:~/auto_template/sample$ make<br/>
rm -f ./src/Y/class_Y_def.o ./src/Y/class_Y.o ./src/X/class_X.o ./src/X/class_X_def.o ./src/main.o<br/>
rm -f bin/sample<br/>
rm -f<br/>
ctags -R<br/>
g++ -c -Wall -g src/Y/class_Y_def.cpp -o src/Y/class_Y_def.o<br/>
g++ -c -Wall -g src/Y/class_Y.cpp -o src/Y/class_Y.o<br/>
g++ -c -Wall -g src/X/class_X.cpp -o src/X/class_X.o<br/>
g++ -c -Wall -g src/X/class_X_def.cpp -o src/X/class_X_def.o<br/>
g++ -c -Wall -g src/main.cpp -o src/main.o<br/>
g++  ./src/Y/class_Y_def.o ./src/Y/class_Y.o ./src/X/class_X.o ./src/X/class_X_def.o ./src/main.o -o bin/sample<br/>
<br/>
Running  “nm –C ./bin/sample” shows this:<br/>
<br/>
0000000000400df9 t __static_initialization_and_destruction_0(int, int)<br/>
                 U operator delete(void*)@@GLIBCXX_3.4<br/>
0000000000400c1e W X<float>::getVal()<br/>
0000000000400c36 W X<float>::setVal(float)<br/>
0000000000400bfc W X<float>::X(float)<br/>
0000000000400c14 W X<float>::X()<br/>
0000000000400bfc W X<float>::X(float)<br/>
0000000000400c14 W X<float>::X()<br/>
0000000000400bd6 W X<int>::getVal()<br/>
0000000000400be6 W X<int>::setVal(int)<br/>
0000000000400bb6 W X<int>::X(int)<br/>
0000000000400bcc W X<int>::X()<br/>
0000000000400bb6 W X<int>::X(int)<br/>
0000000000400bcc W X<int>::X()<br/>
0000000000400a94 W Y<char>::getVal()<br/>
0000000000400aa6 W Y<char>::setVal(char)<br/>
0000000000400a70 W Y<char>::Y(char)<br/>
0000000000400a8a W Y<char>::Y()<br/>
0000000000400a70 W Y<char>::Y(char)<br/>
0000000000400a8a W Y<char>::Y()<br/><br/>



