CC=gcc
CFLAGS=-c -Wall
LDFLAGS=-lGL -lglut -lGLU


all: chip8 

chip8: main.o chip8.o
	$(CC) main.o chip8.o $(LDFLAGS) -o chip8
main.o: main.cpp
	$(CC) $(CFLAGS) main.cpp
chip8.o: chip8.cpp
	$(CC) $(CFLAGS) chip8.cpp

