class function_inlining_trivial_1 {
	def inlined( a:Int, b:Int ): Int = {
		return a+b;
	}

	def function_inlining_trivial_1(input0:Int, input1:Int): Int = {
		return inlined(input0, input1);
	}
}
