1. is this a relevant optimization that could transform two pieces of
   code into the same thing?
   	why / why not?
2. what parts of code can this apply to?
	- all lines (assumed by default)
	- between functions: inter-function
	- loops, etc
	- might apply only to instruction level so it may not be relevant
3. what is there a general name for this optimization?


Resources:
General optimizations:
https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
Details on Tree-SSA passes:
https://gcc.gnu.org/onlinedocs//gccint/Tree-SSA-passes.html
