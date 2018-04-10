class function_inlining_partial_2 {
def inline_this(input0:Array[Int]){
	if(input0 != null){
		input0(0) = 1;
	}
}
def function_inlining_partial(input0:Array[Int]){
	inline_this(input0);
}
}
