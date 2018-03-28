#include <assert.h>
#include <stdio.h>

 int a(int input0, int input1, int input2){
    if(  (input0<0 && !(input1<0)) 
        || 
          (!(input0<0) && input1<0)
    ){
         return -input2; 
    } else {
        return input2;
    }
}

 int b(int input0, int input1, int input2){
     int neg = 0; 
     if(input0<0){neg=!neg;} 
     if(input1<0){neg=!neg;} 
     if(neg!=0){ input2 = -input2;}
     return input2;
}

int main(int argc, char** argv){
	int num = 1234;
	assert( a(-1, -1, num) == b(-1,-1, num) );
	assert( a(1, -1, num) == b(1,-1, num) );
	assert( a(-1, 1, num) == b(-1,1, num) );
	assert( a(1, 1, num) == b(1,1, num) );
	printf("success!\n");
}
