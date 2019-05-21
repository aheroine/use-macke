"""
Storage for all global constants
"""

# A list of flags used by KLEE runs
KLEEFLAGS = [
    "--allow-external-sym-calls",
    "--libc=uclibc",
    "--max-memory=1000",
    "--only-output-states-covering-new",
    "--optimize",
    "--disable-inlining",
    # "--output-module",  # Helpful for debugging
    "--output-source=false",  # Removing this is helpful for debugging
    "--posix-runtime",
    "--watchdog"
]
#jl for main functions
USE_MAIN_FLAGS = [
    "--libc=uclibc",
    "--posix-runtime"
]
#jl for isolute functions not named 
USEFLAGS = [
    "--libc=uclibc"
]

UCLIBC_LIBS = [
    "acl", "crypt", "dl", "m", "pthread", "rt", "selinux"
]

FUZZFUNCDIR_PREFIX = "fuzz_out_"

# A list of file extensions for errors that can be prepended by phase two
#jl debug:more err should be added for use
ERRORFILEEXTENSIONS = [
    ".data.err", ".ctrl.err", ".unified.ptr.err", 
    ".unified.abort.err", ".unified.external.err",
    ".unified.overshift.err", ".newintro.ptr.err",
    ".ptr.err", ".free.err", ".assert.err", ".div.err", ".macke.err", ".fuzz.err"]
USEERRORFILEEXTENSIONS = [
    ".data.err", ".ctrl.err",
    ".ptr.err", ".free.err", ".assert.err", ".div.err", ".macke.err", ".fuzz.err"]
    #jl add .data.err  .ctrl.err
