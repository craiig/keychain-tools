class wrap {
static java.lang.String LINE_SEPARATOR = "\n";
public static java.lang.String wrap( java.lang.String str, int wrapLength, java.lang.String newLineStr, boolean wrapLongWords )
{
	if (str == null) {
		return null;
	}
	if (newLineStr == null) {
		newLineStr = LINE_SEPARATOR;
	}
	if (wrapLength < 1) {
		wrapLength = 1;
	}
	int inputLineLength = str.length();
	int offset = 0;
	java.lang.StringBuffer wrappedLine = new java.lang.StringBuffer( inputLineLength + 32 );
	while (inputLineLength - offset > wrapLength) {
		if (str.charAt( offset ) == ' ') {
			offset++;
			continue;
		}
		int spaceToWrapAt = str.lastIndexOf( ' ', wrapLength + offset );
		if (spaceToWrapAt >= offset) {
			wrappedLine.append( str.substring( offset, spaceToWrapAt ) );
			wrappedLine.append( newLineStr );
			offset = spaceToWrapAt + 1;
		} else {
			if (wrapLongWords) {
				wrappedLine.append( str.substring( offset, wrapLength + offset ) );
				wrappedLine.append( newLineStr );
				offset += wrapLength;
			} else {
				spaceToWrapAt = str.indexOf( ' ', wrapLength + offset );
				if (spaceToWrapAt >= 0) {
					wrappedLine.append( str.substring( offset, spaceToWrapAt ) );
					wrappedLine.append( newLineStr );
					offset = spaceToWrapAt + 1;
				} else {
					wrappedLine.append( str.substring( offset ) );
					offset = inputLineLength;
				}
			}
		}
	}
	wrappedLine.append( str.substring( offset ) );
	return wrappedLine.toString();
}
}
