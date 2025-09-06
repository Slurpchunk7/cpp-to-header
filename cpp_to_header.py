import re
import os
import sys

def strip_function_bodies(content):
    """
    Replaces function bodies with semicolons, leaving only declarations.
    Works with nested braces and multi-line functions.
    """
    result = []
    i = 0
    while i < len(content):
        if content[i] == '{':
            j = i - 1
            while j >= 0 and content[j].isspace():
                j -= 1
            if j >= 0 and content[j] == ')':
                brace_count = 1
                i += 1
                while i < len(content) and brace_count > 0:
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                    i += 1
                result.append(';')
                continue
        result.append(content[i])
        i += 1
    return "".join(result)

def extract_classes(content):
    class_pattern = r'(template\s*<[^>]+>\s*)?(class|struct)\s+\w+\s*(:[^{]+)?\s*{'
    classes = []
    for match in re.finditer(class_pattern, content):
        start = match.start()
        brace_count = 0
        i = match.end() - 1
        while i < len(content):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    classes.append(content[start:i+1] + ';')
                    break
            i += 1
    return classes

def extract_includes(content):
    return re.findall(r'^\s*#include.*', content, re.MULTILINE)

def extract_global_declarations(content):
    decl_pattern = r'^[\w:<>\*&]+\s+\w+\s*(?:\([^)]*\))?\s*(?:=\s*[^;]+)?;'
    return re.findall(decl_pattern, content, re.MULTILINE)

def cpp_to_header(cpp_file):
    with open(cpp_file, 'r') as f:
        content = f.read()
    
    header_lines = [f"#pragma once\n", f"// Generated from {os.path.basename(cpp_file)}\n\n"]
    
    includes = extract_includes(content)
    header_lines.extend(includes)
    header_lines.append("\n")
    
    content_no_bodies = strip_function_bodies(content)
    
    classes = extract_classes(content_no_bodies)
    header_lines.extend(classes)
    header_lines.append("\n")
    
    globals_and_funcs = extract_global_declarations(content_no_bodies)
    header_lines.extend(globals_and_funcs)
    
    header_file = os.path.splitext(cpp_file)[0] + ".h"
    with open(header_file, 'w') as f:
        f.write("\n".join(header_lines))
    
    print(f"Header file created: {header_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cpp_to_h.py <file.cpp>")
    else:
        cpp_to_header(sys.argv[1])
