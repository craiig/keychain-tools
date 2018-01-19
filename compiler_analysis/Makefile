

all:

build/:
	mkdir -p $@

build/llvm_passes.html: build/
	curl -L -o $@ http://llvm.org/docs/Passes.html

build/gcc_optimizations.html: build/
	curl -L -o $@ https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
