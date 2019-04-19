"""
Functions, that wraps all llvm actions and transformation into python functions
"""
import json
import subprocess

from .config import LIBMACKEOPT, LLVMOPT


def __run_subprocess(popenargs):
    """
    Starts a subprocess with popenargs and returns it output
    """
    return subprocess.check_output(popenargs)


def __run_subprocess_json_output(popenargs):
    """
    Starts a subprocess with popenargs and returns the output as parsed json
    """
    out = __run_subprocess(popenargs)
    return json.loads(out.decode("utf-8"))


def list_all_funcs_topological(bitcodefile):
    """
    Wrapper around the list all functions pass. Any circles or strongly
    connected components are listed alphabetically in nested lists
    """
    return __run_subprocess_json_output([
        LLVMOPT, "-load", LIBMACKEOPT,
        "-listallfuncstopologic", bitcodefile,
        "-disable-output"])


def extract_callgraph(bitcodefile):
    """
    Wrapper around the extract callgraph pass
    """
    return __run_subprocess_json_output([
        LLVMOPT, "-load", LIBMACKEOPT,
        "-extractcallgraph", bitcodefile,
        "-disable-output"])


def encapsulate_symbolic(sourcefile, function, destfile=None):
    """
    Wrapper around the encapsulate symbolic pass
    """
    # If no destfile is given, just modify the source file
    if destfile is None:
        destfile = sourcefile

    return __run_subprocess([
        LLVMOPT, "-load", LIBMACKEOPT,
        "-encapsulatesymbolic", sourcefile,
        "-encapsulatedfunction", function, "-o", destfile])


def prepend_error_from_dir(sourcefile, function, errordirlist, destfile=None):
    """
    Wrapper around the prepend error pass
    """
    # Reject empty error lists
    print("DEBUG: ","prepend_error_from_dir",sourcefile,function,errordirlist,destfile)
    assert errordirlist

    # If no destfile is given, just modify the source file
    if destfile is None:
        destfile = sourcefile

    errordirflags = []
    for errordir in errordirlist:
        errordirflags.append("-previouskleerundirectory")
        errordirflags.append(errordir)

    return __run_subprocess([
        LLVMOPT, "-load", LIBMACKEOPT, "-preprenderror", sourcefile,
        "-prependtofunction", function] + errordirflags + ["-o", destfile])


def prepend_error_from_ktest(sourcefile, function, ktestlist, destfile=None):
    """
    Wrapper around the prepend error pass
    """
    # Reject empty ktest lists
    
    assert ktestlist

    # If no destfile is given, just modify the source file
    if destfile is None:
        destfile = sourcefile

    ktestflags = []
    for ktest in ktestlist:
        ktestflags.append("-errorfiletoprepend")
        ktestflags.append(ktest)
    print("-------here-------------------")
    print("DEBUG:",LLVMOPT, "-load", LIBMACKEOPT, "-preprenderror", sourcefile, "-prependtofunction", function)
    print(ktestflags)
    print("-o", destfile)
    print("DEBUG END")
    return __run_subprocess([
        LLVMOPT, "-load", LIBMACKEOPT, "-preprenderror", sourcefile,
        "-prependtofunction", function] + ktestflags + ["-o", destfile])


def remove_unreachable_from(entrypoint, sourcefile, destfile=None):
    """
    Internalize everything except entrypoint and remove unused code
    """
    # If no destfile is given, just modify the source file
    if destfile is None:
        destfile = sourcefile

    return __run_subprocess([
        LLVMOPT, "-internalize-public-api-list=%s" % entrypoint, sourcefile,
        "-internalize", "-globalopt", "-globaldce", "-o", destfile])


def optimize_redundant_globals(sourcefile, destfile=None):
    """
    Runs an llvm opt pass, that merges all globals with identical content
    """
    # If no destfile is given, just modify the source file
    if destfile is None:
        destfile = sourcefile

    return __run_subprocess([
        LLVMOPT, "-constmerge", sourcefile, "-o", destfile])


def extract_lines_of_code(bitcodefile):
    """
    Extract all lines of code represented inside a bitcode file
    """
    return __run_subprocess_json_output([
        LLVMOPT, "-load", LIBMACKEOPT,
        "-extractlinesofcode", bitcodefile, "-disable-output"])
