from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

# print(f"Result for current directory: {get_files_info("calculator", ".")}")
# print(f"Result for 'pkg' directory: {get_files_info("calculator", "pkg")}")
# print(f"Result for '/bin' directory: {get_files_info("calculator", "/bin")}")
# print(f"Result for '../' directory: {get_files_info("calculator", "../")}")

# print(get_file_content("calculator", "lorem.txt"))

# print(get_file_content("calculator", "main.py"))
# print(get_file_content("calculator", "pkg/calculator.py"))
# print(get_file_content("calculator", "/bin/cat"))
# print(get_file_content("calculator", "pkg/does_not_exist.py"))

# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

# print(run_python_file("calculator", "main.py"))  # (should print the calculator's usage instructions)
# print(run_python_file("calculator", "main.py", ["3 + 5"]))  # (should run the calculator... which gives a kinda nasty rendered result)
# print(run_python_file("calculator", "tests.py"))
# print(run_python_file("calculator", "../main.py"))  # (this should return an error)
# print(run_python_file("calculator", "nonexistent.py"))  # (this should return an error)


print(get_file_content({'file_path': 'main.py'}))
print(write_file({'file_path': 'main.txt', 'content': 'hello'}))
print(run_python_file({'file_path': 'main.py'}))
print(get_files_info({'directory': 'pkg'}))