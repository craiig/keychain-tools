# Usage
1. To produce the set of categories used in the paper, run `make analyze`
2. To re-do any of the steps performed to achieve the analysis, see below

## Usage to generate mutants
1. Run `make` to unpack all dependent files and run the mujava interface that
can be used to generate the mutants.
2. In Mujava gui, Check off all .java source files on the left, there should be
   six.
3. Check off all Method-level mutations
3. Click generate and wait. Watch the terminal. Errors are OK. Wait for `all
   files are handled` message. This can take a while (~10mins) because Pamvotis
   in particular generates a large number of variants.
4. Close the Java GUI to continue the Makefile process (don't ctrl+C in the
   terminal).

## Perform variant level analysis
1. Run `make analyze` to start the analysis loop. Read the questions and write down tags until done
2. After tagging, an overall analysis will be run that analyzes each tag and
   generates higher level categories. Edit the `categorize_variants` function
   in do_manual_analysis.py to change tags 

# Requirements
1. make, java
2. maven (to build test samples)

# Attribution
Most files in this directory were downloaded from:
1. http://pages.cs.aueb.gr/~kintism/papers/tce/
2. http://pages.cs.aueb.gr/~kintism/papers/tce/equivalents.html
3. https://cs.gmu.edu/~offutt/mujava/index-v3-nov2008.html

These sources were based on the paper:
> Mike Papadakis, Yue Jia, Mark Harman, and Yves Le Traon. 2015. Trivial
> compiler equivalence: a large scale empirical study of a simple, fast and
> effective equivalent mutant detection technique. In Proceedings of the 37th
> International Conference on Software Engineering - Volume 1 (ICSE '15), Vol.
> 1. IEEE Press, Piscataway, NJ, USA, 936-946.

To eliminate external dependencies and improve reproducibility, many of the
relevant files are already downloaded and added to this repo. Consult the
Makefile to find their particular origin.

To re-download all supporting files and run experiments: `make deep-clean && make`

## Modifications
I added a Makefile that downloads and runs the infrastructure to generate the
manually verified variants listed at
http://pages.cs.aueb.gr/~kintism/papers/tce/equivalents.html.

# Troubleshooting
It appears that sometimes mujava experiences several null exceptions when trying
to enumerate one of it' GUI lists. I found that running `make clean` can help
fix this.
