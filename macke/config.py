"""
Load global configurations, if they exist in a config.ini file
"""

import configparser
import subprocess
from os import path

CONFIG = configparser.ConfigParser()
CONFIGFILE = path.join(path.dirname(__file__), "..", "config.ini")
CONFIG.read(CONFIGFILE)


# for fuzzer
LIBMACKEFUZZPATH = path.expanduser(CONFIG.get("binaries", "libmackefuzzopt"))
LIBMACKEFUZZOPT = path.join(LIBMACKEFUZZPATH, "bin", "libMackeFuzzerOpt.so")
AFLLIB = path.expanduser(CONFIG.get("binaries", "afl-lib"))
AFLBIN = path.expanduser(CONFIG.get("binaries", "afl-bin"))
AFLCC = path.join(AFLBIN, "afl-clang-fast")
AFLFUZZ = path.join(AFLBIN, "afl-fuzz")
AFLTMIN = path.join(AFLBIN, "afl-tmin")
LLVMCONFIG = path.expanduser(CONFIG.get("binaries", "llvm-config"))
LLVMBINDIR = subprocess.check_output([LLVMCONFIG, "--bindir"]).decode("utf-8").strip()
CLANG = path.join(LLVMBINDIR, "clang")
LLVMFUZZOPT = path.join(LLVMBINDIR, "opt")

VALGRIND = path.expanduser(CONFIG.get("binaries", "valgrind"))

# for symbolic execution
LIBMACKEOPT = path.expanduser(CONFIG.get("binaries", "libmackeopt"))
LLVMOPT = path.expanduser(CONFIG.get("binaries", "llvmopt", fallback="opt"))
KLEEBIN = path.expanduser(CONFIG.get("binaries", "klee", fallback="klee"))

# general
THREADNUM = CONFIG.getint("runtime", "threadnum", fallback=None)
FUZZMEMLIMIT = CONFIG.getint("runtime", "memlimit", fallback=50)


def __get_output_from(*args, **kwargs):
    """
    Starts a subprocess with the given args and returns its output - no matter
    if the process exits normally or with an error
    """
    # Sadly, some programs return their help pages with non-zero exit code
    try:
        output = subprocess.check_output(*args, **kwargs)
    except subprocess.CalledProcessError as ex:
        output = ex.output
    return output


def check_config():
    """
    Checks all variables in the config. Especially if all given binaries are
    actually executable, have the correct version and support everything needed
    """

    # Check, if LLVMOPT is actually a binary of opt
    if (not path.isfile(LLVMOPT) or b"llvm .bc -> .bc modular optimizer"
            not in __get_output_from([LLVMOPT, "-help"])):
        raise Exception("Config: Invalid opt binary")

    # Check, if LLVMOPT is the correct opt version
    if b"LLVM version 3.4.2" not in __get_output_from([LLVMOPT, "-version"]):
        raise Exception("Config: Invalid opt version")

    # Check, if LIBMACKEOPT actually supports the relevant passes
    if not path.isfile(LIBMACKEOPT):
        raise Exception("Config: Invalid libmackeopt binary")
    mhelp = __get_output_from([LLVMOPT, "-load", LIBMACKEOPT, "-help"])
    if any(t not in mhelp for t in [
            b"-extractcallgraph", b"-listallfuncstopologic",
            b"-encapsulatesymbolic", b"-preprenderror"]):
        raise Exception(
            "Config: limackeopt does not support all required passes")

    # Check, if KLEEBIN
    if not path.isfile(KLEEBIN):
        raise Exception("Config: Invalid KLEE binary")
    kvers = __get_output_from([KLEEBIN, "-version"])
    if b"KLEE" not in kvers or b"LLVM version 3.4.2" not in kvers:
        raise Exception("Config: Invalid klee version")
    khelp = __get_output_from([KLEEBIN, "-help"])
    if any(t not in khelp for t in [b"=sonar", b"-sonar-target", b"-sonar-target-info=<string>"]):
        raise Exception("Config: klee does not support sonar search")

    # Check, if a reasonable number of threads is used
    if THREADNUM is not None and not 0 < THREADNUM < 128:
        raise Exception("Config: Invalid Number of threads")


def get_current_git_hash_from(directory):
    """
    Returns the git hash of the currently checked out commit in directory
    """
    try:
        githash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=directory,
            stderr=subprocess.DEVNULL).decode("utf-8").rstrip()
    except subprocess.CalledProcessError:
        githash = "unknown"

    return githash


def get_current_git_hash():
    """
    Returns the git hash of the currently checked out commit
    """
    return get_current_git_hash_from(path.join(path.dirname(__file__), ".."))


def get_llvm_opt_git_hash():
    """
    Tries to get the git hash of currently checket out version of
    macke-llvm-opt, if the binary is inside the git repository
    """
    return get_current_git_hash_from(path.dirname(LIBMACKEOPT))


def get_klee_git_hash():
    """
    Tries to get the git hash of currently checket out version of klee,
    if the binary is inside the git repository
    """
    return get_current_git_hash_from(path.dirname(KLEEBIN))
