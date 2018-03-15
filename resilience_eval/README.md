Purpose of resilience test is:
determine the state of syntactic resilience in different compilers with
benchmarks derived from data processing workloads and applicable compiler
transformations.

to demonstrate that compilers are resilient to many differences in syntax
to find areas where some compilers could do better


other projects such as
Finding Missed Compiler Optimizations by
Differential Testing
and Csmith
and TCE
all use randomized testing to evaluate compilers.
these tools evaluate the overall coverage of a compiler with respect to
correctness [csmith], optimizations [difftesting], or program heuristics [tce].
however, we are specially interested to understand if two different programs
*written by different users* will compile to the same syntax. no amount of randomized
testing will provide an answer, because we must qualitatively determine (for
every program) if any other programs in the testing corpus could have
REALISITCALLY been written differently. instead, we performed a
qualitative study to develop a set of syntactically different but equivalent
programs to evaluate compilers with.
external and internal validity (from FSE paper)

interested not in the overall compiler coverage

benchmark details:
1. compiler survey: compilers are not guaranteed to produce the *same* code
   even though they apply the same optimization.
   this shows that many compiler optimizations can generate the same code as
   hand written equivalents.
2. TCE - the hardest benchmarks, larger non-data processing program
3. TPC-DS - representative of expressions used in data processing. 
	not neccessarily of larger control flow, though
4. TODO: ETL workloads???? string manip etc

findings:
1. compiler transformations can effectively canonicalize different syntax to the
   same program. (compilers are not guaranteed to produce the same code by
   they often do)
2. all compilers syntactic could be improved through more canonicalization in
   different cases.
3. there is opportunity for passes solely to improve syntactic resilience:
   compilers can't and shouldn't canonicalize code with early exit conditions,
   different memory allocation patterns, etc. but this could be done to help
   improve resilience.
