class interprocedural_constant_propagation_1 {
	def ipa_cp_inlined(x:Int, y:Int, c:Int): Int = {
		return x+y+c;
	}
	def interprocedural_constant_propagation_1(input0:Int, input1:Int): Int = {
		return ipa_cp_inlined(input0, input1, 1);
	}
}
