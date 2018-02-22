{
	"programs": [
		{
			"name": "constant_folding basic",
			"origin": "tpcds_survey",
			"input_types": ["int"],
			"return_type": "boolean",
			"variants": [
				{ "code": "input0 == 10" }
				, { "code": "input0 == 1+1+8" }
				, { "code": "input0 == 8+1+1" }
				, { "code": "input0 == 2*5" }
				, { "code": "input0 == 5*2" }
			]
		}
		, {
			"name": "constant_folding_associativity",
			"origin": "craig",
			"input_types": ["int", "int"],
			"return_type": "boolean",
			"variants": [
				{ "code": "input0 == input1+2" }
				, { "code": "input0 == input1+1+1" }
				, { "code": "input0 == input1+(1+1)" }
				, { "code": "input0 == 1+1+input1" }
				, { "code": "input0 == (1+1)+input1" }
				, { "code": "input0 == 2+input1" }
			]
		}
		, {
			"name": "comparison",
			"origin": "tpcds_survey",
			"input_types": ["int"],
			"return_type": "boolean",
			"variants": [
				{ "code": "input0 == 10" }
				, { "code": "10 == input0" }
			]
		}
		, {
			"name": "conditional",
			"origin": "tpcds_survey",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "if( input0 == 10 ){ return input1; } else { return 100; }" }
				, { "code": "if( input0 != 10 ){ return 100; } else { return input1; }" }
			]
		}
		, {
			"name": "logical_op",
			"origin": "tpcds_survey",
			"input_types": ["int","int"],
			"return_type": "boolean",
			"variants": [
				{ "code": "(input0 == 10) && (input1 == 20)" }
				, { "code": "(input1 == 20) && (input0 == 10)" }
				, { "code": "!((input1 != 20) || (input0 != 10))" }
			]
		}
		, {
			"name": "math_sub",
			"origin": "tpcds_survey",
			"input_types": ["int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "input0 - input1" }
				, { "code": "-1 * (input1 - input0)" }
			]
		}
		, {
			"name": "math_add",
			"origin": "craig",
			"input_types": ["int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "input0 + input1" }
				, { "code": "input1 + input0" }
			]
		}
		, {
			"name": "function_inlining_trivial",
			"origin": "compiler_survey",
			"notes": "TODO these ARE equivalent but we need to better parse the asm code to demonstrate that",
			"input_types": ["int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "input0 + input1" }
				, { "type": "file", "c": "./benchmarks/function_inlining_1.c" }
			]
		}
		, {
			"name": "common_subexpression_elimination",
			"origin": "compiler_survey",
			"note": "trying to cover -fgcse",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int w = (input0*input1); int x = (w) + 1234; int y = (w) + 5678; return x+y;" }
				, { "code": "int x = (input0 * input1) + 1234; int y = (input0 * input1) + 5678; return x+y;" }
			]
		}
		, {
			"name": "copy_propagation",
			"origin": "compiler_survey",
			"note": "trying to cover -fgcse",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int w = (input0*input1); int x = (w) + 1234; int y = (w) + 5678; return x+y;" }
				, { "code": "int w = (input0*input1); int w2 = w; int x = (w) + 1234; int y = (w2) + 5678; return x+y;" }
			]
		}
		, {
			"name": "constant_propagation",
			"origin": "compiler_survey",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int w = (input0*input1); int x = (w) + 1234; int y = (w) + 5678; return x+y;" }
				, { "code": "int a = 1200+34; int b = 5600+78; int w = (input0*input1); int w2 = w; int x = (w) + a; int y = (w2) + b; return x+y;" }
			]
		}
		, {
			"name": "gcse_kill_load_store_in_loop",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fgcse-lm",
			"input_types": ["int*", "int", "int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x; for(int i=0; i<input1; i++){ *input0 = i; x = *input0; }; return x; " }
				, { "code": "int x; for(int i=0; i<input1; i++){ *input0 = i; x = i; }; return x; " }
			]
		}
		, {
			"name": "gcse_kill_load_after_stores",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fgcse-las",
			"input_types": ["int*", "int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "*input0 = *input1; return *input0;" }
				, { "code": "*input0 = *input1; return *input1;" }
			]
		}
		, {
			"name": "dead_code_elimination",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fdce",
			"input_types": ["int*", "int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "return *input0 + *input1" }
				, { "code": "int x = 100; return *input0 + *input1;" }
				, { "code": "int x = 100; for(int i=0; i<x; i++){ if(i==101){ return x; } } return *input0 + *input1;" }
			]
		}
		, {
			"name": "dead_store_elimination",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fdse",
			"input_types": ["int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "*input0 = 200; return *input0" }
				, { "code": "*input0 = 100; *input0 = 200; return *input0" }
			]
		}
		, {
			"name": "tree_reassociation_subtraction_reassociation",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-reassoc subtraction case",
			"input_types": ["int", "int", "int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "(input0+input1)-(input2+input3)" }
				,{ "code": "(((input0+input1)-input2)-input3)" }
				,{ "code": "(input0+input1-input2)-input3" }
			]
		}
		, {
			"name": "tree_reassociation_linearization",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-reassoc linearization",
			"input_types": ["int", "int", "int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "(input0+input1)+(input2+input3)" }
				,{ "code": "(((input0+input1)+input2)+input3)" }
				,{ "code": "(input0+input1+input2)+input3" }
			]
		}
		, {
			"name": "tree_reassociation_operand_lists",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-reassoc subtraction case",
			"input_types": ["int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "input0 + -input1" }
				, { "code": "input0 - input1" }
				, { "code": "input0 - (input1 & input1)" }
			]
		}
		, {
			"name": "tree_reassociation_repeated_factors",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-reassoc repeated factors",
			"input_types": ["int"],
			"return_type": "int",
			"variants": [
				{ "code": "(input0 * input0 * input0) + (input0 * input0 * input0)" }
				, { "code": "2*(input0 * input0 * input0)" }
			]
		}
		, {
			"name": "code_hoisting",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fcode-hoisting",
			"input_types": ["int*", "int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x = *input0; if(x > 100){ *input0 = x*x; *input1 = 0; } else { *input0 = x*x; *input1 = 1; } " }
				, { "code": "int x = *input0;  *input0 = x*x; if(x > 100){ *input1 = 0; } else { *input1 = 1; } " }
			]
		}
		, {
			"name": "pre",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fpre, tree-ssa-pre.c, example pulled from https://cs.wheaton.edu/~tvandrun/writings/cc04.pdf. this fails in a really weird way on gcc but works on llvm! this is great!",
			"input_types": ["int", "int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int c = input0 + input1; int d; if(input2){ c = input0; d = c + input1; } else { c = 5; } return c + input1; " }
				, { "code": "int c = input0 + input1; int d,t; if(input2){ c = input0; d = c + input1; t = d; } else { c = 5; t = c + input1; } return t; " }
			]
		}
		, {
			"name": "forward_prop",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-forwprop",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x = input0 & input1; if(x){ return 0; } else { return 1; }" } 
				, { "code": "if(input0 & input1){ return 0; } else { return 1; }" } 
			]
		}
		, {
			"name": "fre",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-fre, example based on global value numbering: https://courses.cs.washington.edu/courses/cse501/04wi/papers/click-pldi95.pdf",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x = input0 * input1 + input1; int y = input0 * input1 + input0; return x+y;" }
				, { "code": "int a = input0*input1; int x = a + input1; int y = a + input0; return x+y;" }
			]
		}
		, {
			"name": "copy_propagation",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-copy-prop, TODO improve",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x = input0 * input1; int y = x; return y;" }
				, { "code": "return input0*input1;" }
			]
		}
		, {
			"name": "ipa_cp",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -fipa-cp. TODO this are equivalent but we need to better parse the insns to understand it",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "return input0+input1+1;" }
				, { "type": "file", "c": "./benchmarks/ipa_cp_1.c" }
			]
		}
		, {
			"name": "forward_store_motion",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-sink. example from gcc/tree-ssa-sink.c",
			"input_types": ["int*", "int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int ret; *input0 = input1; input1 = input1 + 1; if(input2){ *input0 = 123; } else { ret = *input0; } return ret;"  }
				, { "code": "int ret; int sinktemp = input1; input1 = input1 + 1; if(input2){ *input0 = 123; } else { *input0 = sinktemp; ret = *input0; } return ret;"  }
			]
		}
		, {
			"name": "ccp",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-ccp. example from gcc/tree-ssa-ccp.c",
			"input_types": ["int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x = 100; if(input0>0 || input0<=0){ x=200; } else { x=300; } return x;"  }
				, { "code": "return 200;"  }
				, { "code": "int x; if(1){ x=200; } else { x=300; } return x;"  }
			]
		}
		, {
			"name": "dce",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-dce. example from gcc/tree-ssa-dce.c",
			"input_types": ["int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "return 100;" }
				, { "code": "int x=1; if(input0){ x=2; } else { x=3; } return 100;" }
			]
		}
		, {
			"name": "dse",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-dse. see gcc/tree-ssa-dse.c",
			"input_types": ["int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "*input0 = 100; *input0 = 200;" }
				, { "code": "*input0 = 200;" }
			]
		}
		, {
			"name": "loop_unswitch",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-loop-optimize. example from gcc/tree-ssa-loop-unswitch.c TODO revisit",
			"input_types": ["int", "int", "int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x=0; for(int i=0; i<input0; i++){ if(input1){ x++; } else { x--; } } return x;" }
				, { "code": "int x=0; if(input1){ for(int i=0; i<input0; i++) x++; } else { for(int i=0; i<input0; i++) x--; } return x; " }
			]
		}
		, {
			"name": "loop_unswitch_harder",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-loop-optimize. example from gcc/tree-ssa-loop-unswitch.c TODO revisit",
			"input_types": ["int", "int", "int*"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x=0; for(int i=0; i<input0; i++){ if(input1){ x++; } else { input2[i] = x--; } } return x;" }
				, { "code": "int x=0; if(input1){ for(int i=0; i<input0; i++) x++; } else { for(int i=0; i<input0; i++) input2[i] = x--; } return x;" }
			]
		}
		, {
			"name": "loop_splitting",
			"origin": "compiler_survey",
			"note": "trying to cover gcc -ftree-loop-optimize. example from gcc/tree-ssa-loop-split.c. WOW this is weird on older clang/gcc, godbolt shows newer clang/gcc are ok",
			"input_types": ["int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x=0; int i; for(i=0; i<200; i++){ if(i<150){ x++; } else { x--; } } return x;" }
				, { "code": "int x=0; int i; for(i=0; i<150; i++){ x++; } for(; i<200; i++){ x--; } return x;" }
			]
		}
		, {
			"name": "for_loop_nothing",
			"origin": "semantics preserving transformations",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "return input0 + input1" }
				, { "code": "return input1 + input0" }
				, { "code": "for(int i=0; i<1; i++){ return input1 + input0; }" }
				, { "code": "int ret = input1; for(int i=0; i<1; i++){ ret += input0; } return ret;" }
			]
		}
		, {
			"name": "math_post_fix_increment",
			"origin": "tce",
			"input_types": ["int", "int"],
			"return_type": "int",
			"variants": [
				{ "code": "input0 + input1" }
				, { "code": "input1++ + input0" }
				, { "code": "input1++ + input0++" }
				, { "code": "input1 + input0++" }
			]
		}
		, {
			"name": "dead_store",
			"origin": "tce",
			"input_types": ["int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "int x = input0 + input1; return x;" }
				, { "code": "int x = input0 * 10; x = input0 + input1; return x;" }
				, { "code": "int x = input0 * 10; if(input0==100) x = 100; else x = input0; return x;" }
			]
		}
		, {
			"name": "dead_store_negate_zero",
			"origin": "tce",
			"input_types": ["int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{ "code": "return input0;" }
				, { "code": "int x = 0; return -x + input0;" }
			]
		}
		, {
			"name": "bisect dead store alternate implementations",
			"origin": "tce",
			"input_types": ["double"],
			"return_type": "double",
			"return": "",
			"variants": [
				{ "java_code": "double N = input0;\n double x = N;\n double M = N;\n double m = 1;\n double r = x;\n double diff = x * x - N;\n while (Math.abs( diff ) > mEpsilon) {\n if (diff < 0) {\n m = x;\n x = (M + x) / 2;\n } else {\n if (diff > 0) {\n M = x;\n x = (m + x) / 2;\n }\n }\n diff = x * x - N;\n }\n r = x;\n mResult = r;\n return r;\n ",
				  "variant_class": "original"}
				, { "java_code": "\n double N = input0;\n double x = N;\n double M = -N;\n double m = 1;\n double r = x;\n double diff = x * x - N;\n while (Math.abs( diff ) > mEpsilon) {\n if (diff < 0) {\n m = x;\n x = (M + x) / 2;\n } else {\n if (diff > 0) {\n M = x;\n x = (m + x) / 2;\n }\n }\n diff = x * x - N;\n }\n r = x;\n mResult = r;\n return r;\n ",
					"variant_class": "negate expression"}
				, { "java_code": "doubt N = input0; \n double x = N;\n double M = N;\n double m = 1;\n double r = x;\n double diff = x * x - N;\n while (Math.abs( diff ) > mEpsilon) {\n if (diff < 0) {\n m = x;\n x = (M + x) / 2;\n } else {\n if (diff != 0) {\n M = x;\n x = (m + x) / 2;\n }\n }\n diff = x * x - N;\n }\n r = x;\n mResult = r;\n return r;\n ", 
					"variant_class": "alternate implementation"}
				, { "java_code": "doubt N = input0; \n double x = N;\n double M = N;\n double m = 1;\n double r = x;\n double diff = x * x - N;\n while (Math.abs( diff ) > mEpsilon) {\n if (diff < 0) {\n m = x;\n x = (M + x) / 2;\n } else {\n if (true) {\n M = x;\n x = (m + x) / 2;\n }\n }\n diff = x * x - N;\n }\n r = x;\n mResult = r;\n return r;\n ",
					"variant_class": "alternate implementation"}
			]
		}
		, {
			"name": "capitalize",
			"origin": "tce",
			"input_types": ["double"],
			"return_type": "double",
			"return": "",
			"variants": [
					{ "java_code": "\n public static java.lang.String capitalize( java.lang.String str, char[] delimiters )\n {\n int delimLen = delimiters == null ? -1 : delimiters.length;\n if (str == null || str.length() == 0 || delimLen == 0) {\n return str;\n }\n int strLen = str.length();\n java.lang.StringBuffer buffer = new java.lang.StringBuffer( strLen );\n boolean capitalizeNext = true;\n for (int i = 0; i < strLen; i++) {\n char ch = str.charAt( i );\n if (isDelimiter( ch, delimiters )) {\n buffer.append( ch );\n capitalizeNext = true;\n } else {\n if (capitalizeNext) {\n buffer.append( Character.toTitleCase( ch ) );\n capitalizeNext = false;\n } else {\n buffer.append( ch );\n }\n }\n }\n return buffer.toString();\n }"
						, "variant_class": "original"
					}
					, { "java_code": "\n public static java.lang.String capitalize( java.lang.String str, char[] delimiters )\n {\n int delimLen = delimiters == null ? 1 : delimiters.length;\n if (str == null || str.length() == 0 || delimLen == 0) {\n return str;\n }\n int strLen = str.length();\n java.lang.StringBuffer buffer = new java.lang.StringBuffer( strLen );\n boolean capitalizeNext = true;\n for (int i = 0; i < strLen; i++) {\n char ch = str.charAt( i );\n if (isDelimiter( ch, delimiters )) {\n buffer.append( ch );\n capitalizeNext = true;\n } else {\n if (capitalizeNext) {\n buffer.append( Character.toTitleCase( ch ) );\n capitalizeNext = false;\n } else {\n buffer.append( ch );\n }\n }\n }\n return buffer.toString();\n }"
						, "variant_class": "early exit removal"
					}
					, { "java_code": "\n public static java.lang.String capitalize( java.lang.String str, char[] delimiters )\n {\n int delimLen = delimiters == null ? -1 : -delimiters.length;\n if (str == null || str.length() == 0 || delimLen == 0) {\n return str;\n }\n int strLen = str.length();\n java.lang.StringBuffer buffer = new java.lang.StringBuffer( strLen );\n boolean capitalizeNext = true;\n for (int i = 0; i < strLen; i++) {\n char ch = str.charAt( i );\n if (isDelimiter( ch, delimiters )) {\n buffer.append( ch );\n capitalizeNext = true;\n } else {\n if (capitalizeNext) {\n buffer.append( Character.toTitleCase( ch ) );\n capitalizeNext = false;\n } else {\n buffer.append( ch );\n }\n }\n }\n return buffer.toString();\n }"
						, "variant_class": "early exit removal"
					}
					, { "java_code": "\n public static java.lang.String capitalize( java.lang.String str, char[] delimiters )\n {\n int delimLen = delimiters == null ? -1 : delimiters.length;\n if (str == null || false || delimLen == 0) {\n return str;\n }\n int strLen = str.length();\n java.lang.StringBuffer buffer = new java.lang.StringBuffer( strLen );\n boolean capitalizeNext = true;\n for (int i = 0; i < strLen; i++) {\n char ch = str.charAt( i );\n if (isDelimiter( ch, delimiters )) {\n buffer.append( ch );\n capitalizeNext = true;\n } else {\n if (capitalizeNext) {\n buffer.append( Character.toTitleCase( ch ) );\n capitalizeNext = false;\n } else {\n buffer.append( ch );\n }\n }\n }\n return buffer.toString();\n }"
						, "variant_class": "early exit removal"
					}
			]
		}
		, {
			"name": "wrap",
			"origin": "tce",
			"input_types": ["String", "int", "String", "boolean"],
			"return_type": "double",
			"return": "",
			"variants": [
				{
					"java_code": "\n public static java.lang.String wrap( java.lang.String str, int wrapLength, java.lang.String newLineStr, boolean wrapLongWords )\n {\n if (str == null) {\n return null;\n }\n if (newLineStr == null) {\n newLineStr = SystemUtils.LINE_SEPARATOR;\n }\n if (wrapLength < 1) {\n wrapLength = 1;\n }\n int inputLineLength = str.length();\n int offset = 0;\n java.lang.StringBuffer wrappedLine = new java.lang.StringBuffer( inputLineLength + 32 );\n while (inputLineLength - offset > wrapLength) {\n if (str.charAt( offset ) == ' ') {\n offset++;\n continue;\n }\n int spaceToWrapAt = str.lastIndexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt >= offset) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n if (wrapLongWords) {\n wrappedLine.append( str.substring( offset, wrapLength + offset ) );\n wrappedLine.append( newLineStr );\n offset += wrapLength;\n } else {\n spaceToWrapAt = str.indexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt >= 0) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n wrappedLine.append( str.substring( offset ) );\n offset = inputLineLength;\n }\n }\n }\n }\n wrappedLine.append( str.substring( offset ) );\n return wrappedLine.toString();\n }\n "
					, "variant_class": "original"
				}
				, {
					"java_code": "\n public static java.lang.String wrap( java.lang.String str, int wrapLength, java.lang.String newLineStr, boolean wrapLongWords )\n {\n if (str == null) {\n return null;\n }\n if (newLineStr == null) {\n newLineStr = SystemUtils.LINE_SEPARATOR;\n }\n if (wrapLength < 1) {\n wrapLength = 1;\n }\n int inputLineLength = str.length();\n int offset = 0;\n java.lang.StringBuffer wrappedLine = new java.lang.StringBuffer( inputLineLength * 32 );\n while (inputLineLength - offset > wrapLength) {\n if (str.charAt( offset ) == ' ') {\n offset++;\n continue;\n }\n int spaceToWrapAt = str.lastIndexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt >= offset) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n if (wrapLongWords) {\n wrappedLine.append( str.substring( offset, wrapLength + offset ) );\n wrappedLine.append( newLineStr );\n offset += wrapLength;\n } else {\n spaceToWrapAt = str.indexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt >= 0) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n wrappedLine.append( str.substring( offset ) );\n offset = inputLineLength;\n }\n }\n }\n }\n wrappedLine.append( str.substring( offset ) );\n return wrappedLine.toString();\n }\n "
					, "variant_class": "memory allocation size change"
				}
				, {
					"java_code": "\n public static java.lang.String wrap( java.lang.String str, int wrapLength, java.lang.String newLineStr, boolean wrapLongWords )\n {\n if (str == null) {\n return null;\n }\n if (newLineStr == null) {\n newLineStr = SystemUtils.LINE_SEPARATOR;\n }\n if (wrapLength < 1) {\n wrapLength = 1;\n }\n int inputLineLength = str.length();\n int offset = 0;\n java.lang.StringBuffer wrappedLine = new java.lang.StringBuffer( inputLineLength + 32 );\n while (inputLineLength - offset > wrapLength) {\n if (str.charAt( offset ) == ' ') {\n offset++;\n continue;\n }\n int spaceToWrapAt = str.lastIndexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt > offset) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n if (wrapLongWords) {\n wrappedLine.append( str.substring( offset, wrapLength + offset ) );\n wrappedLine.append( newLineStr );\n offset += wrapLength;\n } else {\n spaceToWrapAt = str.indexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt >= 0) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n wrappedLine.append( str.substring( offset ) );\n offset = inputLineLength;\n }\n }\n }\n }\n wrappedLine.append( str.substring( offset ) );\n return wrappedLine.toString();\n }\n "
					, "variant_class": "alternate implementation"
				}
				, {
					"java_code": "\n public static java.lang.String wrap( java.lang.String str, int wrapLength, java.lang.String newLineStr, boolean wrapLongWords )\n {\n if (str == null) {\n return null;\n }\n if (newLineStr == null) {\n newLineStr = SystemUtils.LINE_SEPARATOR;\n }\n if (wrapLength < 1) {\n wrapLength = 1;\n }\n int inputLineLength = str.length();\n int offset = 0;\n java.lang.StringBuffer wrappedLine = new java.lang.StringBuffer( inputLineLength + 32 );\n while (inputLineLength - offset > wrapLength) {\n if (str.charAt( offset ) == ' ') {\n offset++;\n continue;\n }\n int spaceToWrapAt = str.lastIndexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt >= offset) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n if (wrapLongWords) {\n wrappedLine.append( str.substring( offset, wrapLength + offset ) );\n wrappedLine.append( newLineStr );\n offset += wrapLength;\n } else {\n spaceToWrapAt = str.indexOf( ' ', wrapLength + offset );\n if (spaceToWrapAt > 0) {\n wrappedLine.append( str.substring( offset, spaceToWrapAt ) );\n wrappedLine.append( newLineStr );\n offset = spaceToWrapAt + 1;\n } else {\n wrappedLine.append( str.substring( offset ) );\n offset = inputLineLength;\n }\n }\n }\n }\n wrappedLine.append( str.substring( offset ) );\n return wrappedLine.toString();\n }\n "
					, "variant_class": "alternate implementation"
				}
			]
		}
		, {
			"name": "add (jodatime)",
			"origin": "tce",
			"input_types": ["long", "int"],
			"return_type": "long",
			"return": "",
			"variants": [
				{
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse == 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "original"
				}
				, {
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( -monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse == 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "negate expression"
				}
				, {
					"java_code": " public long add( long instant, int months )\n {\n if (false) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse == 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "early exit removal"
				}
				, {
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse > 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse == 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "mathematically equivalent"
				}
				, {
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse <= 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "mathematically equivalent"
				}
				, {
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse <= 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "mathematically equivalent"
				}
				, {
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse == 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse <= 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse > maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "mathematically equivalent"
				},
				{
					"java_code": " public long add( long instant, int months )\n {\n if (months == 0) {\n return instant;\n }\n long timePart = 1516149603588; //iChronology.getMillisOfDay( instant );\n int thisYear = 2018; //iChronology.getYear( instant );\n int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );\n int yearToUse;\n int monthToUse = thisMonth - 1 + months;\n if (monthToUse >= 0) {\n yearToUse = thisYear + monthToUse / iMax;\n monthToUse = monthToUse % iMax + 1;\n } else {\n yearToUse = thisYear + monthToUse / iMax - 1;\n monthToUse = Math.abs( monthToUse );\n int remMonthToUse = monthToUse % iMax;\n if (remMonthToUse == 0) {\n remMonthToUse = iMax;\n }\n monthToUse = iMax - remMonthToUse + 1;\n if (monthToUse == 1) {\n yearToUse += 1;\n }\n }\n int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */\n int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */\n if (dayToUse >= maxDay) {\n dayToUse = maxDay;\n }\n /*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );\n return datePart + timePart; */\n return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok\n }\n "
					, "variant_class": "mathematically equivalent"
				}
			]
		}
		, {
			"name": "pamvotis dead store",
			"origin": "tce",
			"input_types": ["int", "int"],
			"return_type": "long",
			"return": "",
			"variants": [
				{
					"code": "int nCwMin = input0;\n switch(input0){\n case 1:\n nCwMin = 1;\n break;\n case 2:\n nCwMin = 2;\n break;\n case 3:\n nCwMin = 3;\n break;\n case 4:\n nCwMin = 4;\n break;\n default:\n nCwMin = 0;\n }\n return nCwMin;\n"
					, "variant_class" : "original"
				}
				, {
					"code": "int nCwMin = -input0;\n switch(input0){\n case 1:\n nCwMin = 1;\n break;\n case 2:\n nCwMin = 2;\n break;\n case 3:\n nCwMin = 3;\n break;\n case 4:\n nCwMin = 4;\n break;\n default:\n nCwMin = 0;\n }\n return nCwMin;\n"
					, "variant_class" : "invert dead store"
				}
				, {
					"code": "int nCwMin = input1 * input0;\n switch(input0){\n case 1:\n nCwMin = 1;\n break;\n case 2:\n nCwMin = 2;\n break;\n case 3:\n nCwMin = 3;\n break;\n case 4:\n nCwMin = 4;\n break;\n default:\n nCwMin = 0;\n }\n return nCwMin;\n"
					, "variant_class" : "math dead store"
				}
			]
		}
		, {
			"name": "pamvotis wider comparison",
			"origin": "tce",
			"input_types": ["int", "int*"],
			"return_type": "int",
			"return": "",
			"notes": "fails, but the difference is in how a 1 is stored in AX, not the comparison op itself, is this a bug? very weird",
			"variants": [
				{
					"code": "\n int position = -1;\n for(int i=0; i<input0; i++){\n if(input1[i] == 0){\n position = i;\n break;\n }\n }\n if(position != -1){\n return 1;\n }\n return 0;\n "
					, "variant_class": "original"
				}
				, {
					"code": "\n int position = -1;\n for(int i=0; i<input0; i++){\n if(input1[i] == 0){\n position = i;\n break;\n }\n }\n if(position > -1){\n return 1;\n }\n return 0;\n "
					, "variant_class": "comparison widening"
				}
			]
		}
		, {
			"name": "triangle classify",
			"origin": "tce",
			"input_types": ["int", "int", "int"],
			"return_type": "int",
			"return": "",
			"variants": [
				{
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "original"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = -trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "invert expression non functional"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = -trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "invert expression functional"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian <= 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "comparison widening"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian >= 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "comparison widening"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 ^ b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "early exit removal"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian == 0) {\n if (a + b < c ^ a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "comparison widening with mathematical proof"
				}
				, {
					"code":"\n int INVALID = 0; \n int SCALENE = 1;\n int EQUILATERAL = 2;\n int ISOSCELES = 3;\n \n int a = input0;\n int b = input1;\n int c = input2;\n \n int trian;\n if (a <= 0 || b <= 0 || c <= 0) {\n return INVALID;\n }\n trian = 0;\n if (a == b) {\n trian = trian + 1;\n }\n if (a == c) {\n trian = trian + 2;\n }\n if (b == c) {\n trian = trian + 3;\n }\n if (trian <= 0) {\n if (a + b < c || a + c < b || b + c < a) {\n return INVALID;\n } else {\n return SCALENE;\n }\n }\n if (trian > 3) {\n return EQUILATERAL;\n }\n if (trian == 1 && a + b > c) {\n return ISOSCELES;\n } else {\n if (trian == 2 && a + c > b) {\n return ISOSCELES;\n } else {\n if (trian == 3 && b + c > a) {\n return ISOSCELES;\n }\n }\n }\n return INVALID;\n "
					, "variant_class": "comparison widening"
				}
			]
		}
		, {
			"name": "xstream decode fast path",
			"origin": "tce",
			"input_types": ["char*"],
			"return_type": "void",
			"return": "",
			"variants": [
				{
					"code": "\n int length = 256;\n char term = '$';\n char term2 = '$';\n int i=0;\n for(; i<length; i++){\n if(input0[i] == term){\n break;\n }\n }\n for(; i<length; i++){\n if(input0[i] == term && input0[i+1] == term2){\n input0[i] = '_'; input0[i+1] = '_';\n }\n }\n ",
					"variant_class": "original"
				}
				, {
					"code": "\n int length = 256;\n char term = '$';\n char term2 = '$';\n int i=0;\n for(; !(i<length); i++){\n if(input0[i] == term){\n break;\n }\n }\n for(; i<length; i++){\n if(input0[i] == term && input0[i+1] == term2){\n input0[i] = '_'; input0[i+1] = '_';\n }\n }\n ",
					"variant_class": "fast path removal"
				}
			]
		}
	]
}
