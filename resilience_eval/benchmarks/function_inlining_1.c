int inlined( int a, int b ){
	return a+b;
}

int function_inlining_trivial(int input0, int input1){
	return inlined(input0, input1);
}
