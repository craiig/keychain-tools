#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <assert.h>

#define clean_errno() (errno == 0 ? "None" : strerror(errno))
#define log_error(M, ...) fprintf(stderr, "[ERROR] (%s:%d: errno: %s) " M "\n", __FILE__, __LINE__, clean_errno(), ##__VA_ARGS__)
#define assertf(A, M, ...) if(!(A)) {log_error(M, ##__VA_ARGS__); assert(A); }

int loop_unswitch_0(int input0, int input1, int* input2){ 
int x=0; for(int i=0; i<input0; i++){ if(input1!=0){ x++; } else { input2[i] = x--; } } return x;
}

int loop_unswitch_1(int input0, int input1, int* input2){ 
int x=0; if(input1!=0){ for(int i=0; i<input0; i++) x++; } else { for(int i=0; i<input0; i++) input2[i] = x--; } return x;
}

void reset_arrays(int* a, int* b, int len){
	for (int i=0; i<len; i++){
		a[i] = 666;
		b[i] = 666;
	}
}

int main(int argc, char** argv){
	int len = 10;
	int array1[len];
	int array2[len];
	int a, b;

	reset_arrays(array1, array2, len);
	printf("cond = 0\n");
	a = loop_unswitch_0(len, 0, array1);
	b = loop_unswitch_1(len, 0, array2);
	for(int i=0; i<len; i++){
		assertf(array1[i] == array2[i], "array1[%d] (%d) == array2[%d] (%d)\n", i, array1[i], i, array2[i]);
		printf("array1[%d] (%d) == array2[%d] (%d)\n", i, array1[i], i, array2[i]);
	}
	printf("returns: %d %d\n", a, b);
	assertf(a == b, "return values don't match %d == %d", a, b);

	reset_arrays(array1, array2, len);
	printf("cond = 1\n");
	a = loop_unswitch_0(len, 1, array1);
	b = loop_unswitch_1(len, 1, array2);
	for(int i=0; i<len; i++){
		assertf(array1[i] == array2[i], "array1[%d] (%d) == array2[%d] (%d)\n", i, array1[i], i, array2[i]);
		printf("array1[%d] (%d) == array2[%d] (%d)\n", i, array1[i], i, array2[i]);
	}
	printf("returns: %d %d\n", a, b);
	assertf(a == b, "return values don't match %d == %d", a, b);

	printf("success!\n");
}
