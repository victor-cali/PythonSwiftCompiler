# Toy Compiler: Python to Swift

This is small compiler to convert python for loops and print statements to Swift for loops and print statements. This compiler accepts any combination of for and print statements as long as it always starts with a loop and finishes with a print statement. for loops must always be of the form "for identifier in range(num1,num2)". print statements can only print identifiers (from the loops) or strings.

The project is implemented in Python 3.8.

To execute it, run the following command inside the project directory:

```
python pyswift.py source_file.py output_file.swift
```
