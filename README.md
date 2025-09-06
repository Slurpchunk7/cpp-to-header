# C++ to Header Generator

This project provides a simple Python script to automatically generate C++ header files (`.h`) from C++ source files (`.cpp`).  

It scans the source file for function definitions and creates a corresponding header file with proper declarations.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
1. Clone or download this repository.
2. Make sure you have **Python 3.6+** installed.
3. Make sure you have `re`, `os` and `sys` installed.

---

## Usage
To generate a header file from a `.cpp` file:

```bash
python cpp_to_header.py yourFile.cpp
