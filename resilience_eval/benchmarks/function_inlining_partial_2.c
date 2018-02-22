#include <stddef.h>
void inline_this(int* input0){
	if(input0 != NULL){
		input0[0] = 1;
	}
}
void function_inlining_partial(int* input0){
	inline_this(input0);
}
