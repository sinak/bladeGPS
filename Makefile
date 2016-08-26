# Makefile for Linux etc.

.PHONY: all clean
all: bladegps

SHELL=/bin/bash
CC=g++
CFLAGS=-O3 -Wall -I../bladeRF/host/libraries/libbladeRF/include -fpermissive
LDFLAGS=-lm -lpthread -L../bladeRF/host/build/output -lbladeRF -lncurses # ncurses required for for getch for now

bladegps: bladegps.o gpssim.o getch.o
	${CC} $^ ${LDFLAGS} -o $@

clean:
	rm -f *.o bladegps
