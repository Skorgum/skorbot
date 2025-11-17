# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test():
    working_directory = "calculator"
    print(run_python_file(working_directory, "main.py"))
    print(run_python_file(working_directory, "main.py", ["3 + 5"]))
    print(run_python_file(working_directory, "tests.py"))
    print(run_python_file(working_directory, "../main.py"))
    print(run_python_file(working_directory, "nonexistent.py"))
    print(run_python_file(working_directory, "lorem.txt"))

if __name__ == "__main__":
    test()
