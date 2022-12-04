# Compiler parameters
CC=g++ # Compiler
CFLAGS=-Wall -std=c++11 -pedantic -g # Compiler flags
LDFLAGS= # Libraries
LDFLAGS_TEST= -I./ -lcppunit
EXEC=prototype.out # Executable name

# Directories
SRC_DIR=src/

# Object files to create
# This finds and enumerate every .cpp files except src/ImageDrawingConverter.cpp and src/console-drawer.cpp (the later file if for later use)
SRCM= $(shell find $(SRC_DIR) -name "*.cpp" ! -name "ImageDrawingConverter.cpp" ! -name "console-drawer.cpp") 
OBJECTS = $(SRCM:.cpp=.o) # This creates an enumeration of .o files for every single .cpp files found 

all: $(EXEC)

run:
	./$(EXEC)

$(EXEC): $(SRC_DIR)/ImageDrawingConverter.o $(OBJECTS) # Linking
	$(CC) -o $@ $^ $(LDFLAGS)
	
%.o: %.cpp %.hpp # Compiling
	$(CC) $(CFLAGS) -o $@ -c $<
 
## Dynamic .o and .out file search
OBJECTS_FILES=$(shell find ./ -name "*.o")
OUT_FILES=$(shell find ./ -name "*.out")

clean:
	rm $(OBJECTS_FILES);\
	rm $(OUT_FILES);