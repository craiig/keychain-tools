class function_inlining_partial_1 {
def inline_this(input0: Array[Int]) = {
	if(input0 != null){
		input0(0) = 1;
	}
}
def function_inlining_partial(input0: Array[Int]) = {
	if(input0 != null){
		inline_this(input0);
	}
}
}
