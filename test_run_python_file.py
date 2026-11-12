from functions.run_python_file import run_python_file

print("Test 1:")
print(run_python_file("calculator", "main.py"))

print("Test 2:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("Test 3:")
print(run_python_file("calculator", "tests.py"))

print("Test 4:")
print(run_python_file("calculator", "../main.py"))

print("Test 5:")
print(run_python_file("calculator", "nonexistent.py"))

print("Test 6:")
print(run_python_file("calculator", "lorem.txt"))