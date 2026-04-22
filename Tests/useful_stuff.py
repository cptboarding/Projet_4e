import sys
import os

def debugger(func, debug_mode=False):
    func_name = func.__name__
    module = sys.modules[func.__module__]
    path = module.__file__
    file_name = os.path.basename(path)

    text = f'Debugging function {func_name} on {file_name} '
    line_separator = "-" * (150-len(text))

    if debug_mode:
        print(text, line_separator)
    if module.__name__ == "__main__":
        if debug_mode:
            print("Output:\n")
        func()
    else:
        if debug_mode:
            print("Debug failed, the function is not in the main file")


    return func
