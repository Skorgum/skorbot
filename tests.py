from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def test():
    working_directory = "calculator"
    print(get_file_content(working_directory, "main.py"))
    print(get_file_content(working_directory, "pkg/calculator.py"))
    print(get_file_content(working_directory, "/bin/cat"))

if __name__ == "__main__":
    test()
