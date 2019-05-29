def parse_error_file(filename, target_function):
    f = open(filename)
    lines = f.readlines()
    error_type = lines[0]

    stack = []
    for i in range(1, len(lines)):
        if lines[i].startswith(Stack:):
            for j in range(i + 1, len(lines)):
                stack.append(lines[j])
                if in %s % target_function in lines[j]:
                    break

    f.close()

    with open(filename+.stack, 'w') as new_f:
        new_f.write(error_type)
        new_f.write(''.join(stack))


import sys

if __name__ == "__main__":
    path = sys.argv[1]
    target = sys.argv[2]
    parse_error_file(path,target)
