

sources := $(wildcard src/*.c)
llvm_bitcode := $(patsubst src/%.c,ll/%.ll,$(sources))
gcc_asm := $(patsubst src/%.c,gcc_asm/%.S,$(sources))

OPT := 
#OPT := -O3

all: $(llvm_bitcode) $(gcc_asm)

ll/%.ll: src/%.c
	clang $< -o $@ -c -S -emit-llvm $(OPT)

gcc_asm/%.S: src/%.c
	gcc $< -o $@ -c -S $(OPT)

.PHONY: clean
clean:
	-rm -rf ll/*.ll
	-rm -rf gcc_asm/*.S
