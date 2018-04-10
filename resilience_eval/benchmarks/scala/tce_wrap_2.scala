import java.lang.String; 
import java.lang.StringBuffer;

class wrap_1 {
val LINE_SEPARATOR = "\n";
def wrap( str:String, _wrapLength:Int, _newLineStr:String, wrapLongWords:Boolean ): String = 
{
	if (str == null) {
		return null;
	}
    var newLineStr = _newLineStr;
	if (newLineStr == null) {
		newLineStr = LINE_SEPARATOR;
	}
    var wrapLength = _wrapLength;
	if (wrapLength < 1) {
		wrapLength = 1;
	}
	val inputLineLength = str.length();
	var offset = 0;
	val wrappedLine = new java.lang.StringBuffer( inputLineLength * 32 );
	while (inputLineLength - offset > wrapLength) {
		if (str.charAt( offset ) == ' ') {
            offset += 1;
		} else {
		var spaceToWrapAt = str.lastIndexOf( ' ', wrapLength + offset );
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
	}
	wrappedLine.append( str.substring( offset ) );
	return wrappedLine.toString();
}
}
