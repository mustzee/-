CXX = g++
CXXFLAGS = -fopenmp -O3 -std=c++17 -Wall
LDFLAGS = -lm

TARGET = parallel_demo
SRC = parallel_demo.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
