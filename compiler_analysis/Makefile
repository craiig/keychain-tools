

all:

review_untagged:
	./tag_optimizations.py --db build/optimizations_db.json -m -mst

review_all:
	./tag_optimizations.py --db build/optimizations_db.json -m

read_gcc: ./build/gcc_optimizations.html
	./tag_optimizations.py --db build/optimizations_db.json --gcc_parse $<

read_llvm: ./build/llvm_passes.html
	./tag_optimizations.py --db build/optimizations_db.json --llvm_parse $<

build/:
	mkdir -p $@

build/llvm_passes.html: | build/
	curl -L -o $@ http://llvm.org/docs/Passes.html

build/gcc_optimizations.html: | build/
	curl -L -o $@ https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
