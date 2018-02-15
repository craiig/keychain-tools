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
