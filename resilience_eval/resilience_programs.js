{
	"programs": [
		{
			"name": "constant_folding_basic",
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
	]
}
