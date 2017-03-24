CC:=g++
CFLAGS:=-c -Wall -g
LDFLAGS:=
SOURCES:=$(shell find -iname "*.cpp")
OBJECTS=$(SOURCES:.cpp=.o)
BINDIR:=bin
EXECUTABLE:=$(BINDIR)/sample
OTHEROBJS = $(shell find -iname "*def.o")

all: clean tags $(SOURCES) $(EXECUTABLE)
    
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

.PHONY:clean
clean:
	rm -f $(OBJECTS)
	rm -f $(EXECUTABLE)
	rm -f $(OTHEROBJS)

.PHONY:tags
tags:
	ctags -R
