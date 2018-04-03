public class function_inlining_trivial_1 {
	int inlined( int a, int b ){
		return a+b;
	}

	public int function_inlining_trivial_1(int input0, int input1){
		return inlined(input0, input1);
	}
}
