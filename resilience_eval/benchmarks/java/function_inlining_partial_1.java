public class function_inlining_partial_1 {
void inline_this(int[] input0){
	if(input0 != null){
		input0[0] = 1;
	}
}
void function_inlining_partial(int[] input0){
	if(input0 != null){
		inline_this(input0);
	}
}
}
