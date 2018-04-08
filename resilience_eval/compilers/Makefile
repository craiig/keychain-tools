all: 
	@echo use this script to help build the compilers you need for testing
	@echo i.e. make clang6 clang7
	@echo FYI these are configured for macos, so you may need to change paths and instructions as needed

gcc7:
	brew install gcc

#clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz:
clang6: ./clang+llvm-6.0.0-x86_64-apple-darwin
clang+llvm-6.0.0-x86_64-apple-darwin: clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz
	tar -vzxf $<
	touch $@

clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz:
	curl -Lo http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz > $@

./llvm/llvm-project:
	mkdir -p ./llvm/
	git clone https://github.com/llvm-project/llvm-project-20170507/ llvm-project
	cd llvm-project && git config branch.master.rebase true

clang7: ./llvm/llvm-project
	mkdir -p ./llvm/clang-build
	mkdir -p ./llvm/clang-install
	cd ./llvm/clang-build && cmake -GNinja ../llvm-project/llvm -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=`pwd`/../clang-install
	#cd ./llvm/clang-build && cmake -GNinja ../llvm-project/llvm -DLLVM_ENABLE_PROJECTS="clang;libcxx;libcxxabi" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=`pwd`/../clang-install
	cd ./llvm/clang-build && ninja install
