1. is this a relevant optimization that could transform two pieces of
   code into the same thing?
   	why / why not?
	many optimizations are possible to implement by hand
		which would canonicalize with non optimize code
		just mark this as non relevant hand optimization in these cases
2. if 1, which level does this optimization apply to?
	i.e will it canonicalize code written for:
	JVM bytecode? Native? 
3. what parts of code can this apply to?
	- all lines (assumed by default)
	- between functions: inter-function
	- loops, etc
	- might apply only to instruction level so it may not be relevant
4. what is there a general name for this optimization?


Resources:
General optimizations:
https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
Details on Tree-SSA passes:
https://gcc.gnu.org/onlinedocs//gccint/Tree-SSA-passes.html
