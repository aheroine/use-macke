CLANG ?= $$HOME/build/llvm/Release/bin/clang

.PHONY: all
all: help

.PHONY: help
help:
	@ echo "Please give a target. Choices are:"
	@ echo "   test -> run all unittests"
	@ echo "   dev  -> installs this project in local virtual environment"
	@ echo "   venv -> update (and if needed initialize) the virual environment"

.PHONY: dev
dev: venv
	.venv/bin/python3 -m pip install --editable .
	@ echo "Everything is set up for development."
	@ echo "Please switch with 'source .venv/bin/activate'"

.PHONY: test
test: venv examples/chain.bc examples/divisible.bc examples/doomcircle.bc \
		examples/factorial.bc examples/justmain.bc examples/main.bc \
		examples/not42.bc examples/sanatized.bc examples/small.bc \
		examples/split.bc
	.venv/bin/python -m unittest

# Initialize the virtual environment, if needed
.venv:
	python3 -m venv .venv --without-pip --system-site-packages
	.venv/bin/python3 -m pip install --upgrade pip

# Install and keep in sync with the requirements
.venv/bin/activate: requirements.txt .venv
	.venv/bin/python3 -m pip install -Ur requirements.txt
	touch .venv/bin/activate

.PHONY: venv
venv: .venv/bin/activate

.PHONY: clean
clean:
	@ rm -rf .venv
	@ rm -rf macke.egg-info
	@ rm -rf macke/__pycache__
	@ rm -rf tests/__pycache__
	@ rm -f examples/*.bc

examples/%.bc: examples/%.c
	$(CLANG) -c -emit-llvm -O0 -g $^ -o $@
