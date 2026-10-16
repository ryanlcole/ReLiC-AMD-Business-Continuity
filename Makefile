CXX ?= g++
CXXFLAGS ?= -std=c++17 -O3 -ffp-contract=off -Wall -Wextra -Iinclude
HIPCC ?= hipcc
HIPFLAGS ?= -std=c++17 -O3 -ffp-contract=off -Iinclude

all: cpu
cpu: bin/runecore_cpu
hip: bin/runecore_hip

bin/runecore_cpu: src/cpu_reference.cpp include/runecore.hpp
	mkdir -p bin evidence
	$(CXX) $(CXXFLAGS) src/cpu_reference.cpp -o $@

bin/runecore_hip: src/hip_runecore.hip.cpp include/runecore.hpp
	mkdir -p bin evidence
	$(HIPCC) $(HIPFLAGS) src/hip_runecore.hip.cpp -o $@

test: cpu
	python3 tests/test_cpu.py

clean:
	rm -rf bin evidence/*.csv evidence/*.json evidence/*.jsonl
.PHONY: all cpu hip test clean
