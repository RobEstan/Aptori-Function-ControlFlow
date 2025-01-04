import ast
import os
import sys


class Primary(ast.NodeVisitor):
    def __init__(self, target_func_name):
        self.target_func_name = target_func_name
        self.in_target_function = False
        self.relevant_functions = []
        self.passed_functions={}
        self.func_lines={}
        self.external_funcs = []
        self.funcs = []

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        self.passed_functions[node.name] = self.funcs
        self.func_lines[node.name] = node.lineno
        self.funcs = []


    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.funcs.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.funcs.append(node.func.attr)
    
    def func_tunneler(self, node):
        if node not in self.relevant_functions: self.relevant_functions.append(node)
        if node in self.passed_functions:
            for func in self.passed_functions[node]:
                if func not in self.relevant_functions:
                    self.relevant_functions.append(func)
                    self.func_tunneler(func)
        else:
            self.relevant_functions.remove(node)
            self.external_funcs.append(node)


def find_possible_files(module_name, search_paths):
   
    possible_files = []
    module_path = module_name.replace('.', os.sep)

    for path in search_paths:
        file_path = os.path.join(path, f"{module_path}.py")
        if os.path.isfile(file_path):
            possible_files.append(file_path)
        
        package_path = os.path.join(path, module_path)
        if os.path.isdir(package_path):
            init_file = os.path.join(package_path, '__init__.py')
            if os.path.isfile(init_file):
                possible_files.append(init_file)
    
    return possible_files
       
def get_called_functions(source_code, target):
    tree = ast.parse(source_code)
    print(ast.dump(tree))
    
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    search_paths = sys.path
    
    visitor = Primary(target)
    visitor.visit(tree) 
    print(visitor.passed_functions)
    #print(visitor.passed_functions)
    for func in visitor.passed_functions[target]:
        visitor.func_tunneler(func)
  
    
    print("Path of Functions: \n")
    print("Line ", visitor.func_lines[target], " func ", target, " - ", visitor.passed_functions[target])

    for func in visitor.relevant_functions:
        if func != target: 
            print("Line ", visitor.func_lines[func], " func ",func, " - ", visitor.passed_functions[func])

    print(f"Functions called within '{target}': {visitor.relevant_functions} \n")
    
    for module_name in imports:
        print(f"Searching for module: {module_name}")
        possible_files = find_possible_files(module_name, search_paths)
        outer_relevant_funcs = []
        if possible_files:
            print(f"Found the following possible files for {module_name}:")
            
            for file in possible_files:
                for func_targ in visitor.external_funcs:
                    
                    print(f" - {file}")
                    with open(file, 'r') as read_file:
                        file_content = read_file.read()
                    file_target = func_targ
                    child_funcs = get_called_functions(file_content, file_target)
                    if not child_funcs == []:
                        outer_relevant_funcs.append(child_funcs)
                    
                    
        else:
            print(f"No files found for module: {module_name}")
        print()

    return visitor.relevant_functions



with open("C:/Users/PanPa/Progaming/Aptori-Function-ControlFlow/Example_5.py", 'r') as file:
    content = file.read()

target = 'foo'
called_functions = get_called_functions(content, target)


"""
Places for Improvement:
My current code is good at digesting and finding every function found in target functions but one area
where it lacks is in distinguishing what type of function is being called. For example functions like 
print() or functions from a math import like min() cause my program to run into errors because it has no
system of detecting wheter a function is defined in the files actually present or defined in a library 
being imported with no readily access files that can be parsed. 
Cannot distinguish between imported functions and overwritten functions.
"""

    