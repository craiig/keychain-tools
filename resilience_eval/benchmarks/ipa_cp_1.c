int ipa_cp_inlined(int x, int y, int c){
	return x+y+c;
}
int ipa_cp(int input0, int input1){
	return ipa_cp_inlined(input0, input1, 1);
}
