class capitalize {
    private static boolean isDelimiter( char ch, char[] delimiters )
    {
        if (delimiters == null) {
            return Character.isWhitespace( ch );
        }
        for (int i = 0, isize = delimiters.length; i < isize; i++) {
            if (ch == delimiters[i]) {
                return true;
            }
        }
        return false;
    }
public static java.lang.String capitalize( java.lang.String str, char[] delimiters )
{
	int delimLen = delimiters == null ? 1 : delimiters.length;
	if (str == null || str.length() == 0 || delimLen == 0) {
		return str;
	}
	int strLen = str.length();
	java.lang.StringBuffer buffer = new java.lang.StringBuffer( strLen );
	boolean capitalizeNext = true;
	for (int i = 0; i < strLen; i++) {
		char ch = str.charAt( i );
		if (isDelimiter( ch, delimiters )) {
			buffer.append( ch );
			capitalizeNext = true;
		} else {
			if (capitalizeNext) {
				buffer.append( Character.toTitleCase( ch ) );
				capitalizeNext = false;
			} else {
				buffer.append( ch );
			}
		}
	}
	return buffer.toString();
}
}
