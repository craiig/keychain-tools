import java.lang.String;
import java.lang.StringBuffer;

class capitalize_0 {
    def isDelimiter( ch:Char, delimiters:Array[Char] ): Boolean =
    {
        if (delimiters == null) {
            return Character.isWhitespace( ch );
        }
        for( i <- 0 until delimiters.length){
            if (ch == delimiters(i)) {
                return true;
            }
        }
        return false;
    }
    def capitalize( str:String, delimiters:Array[Char] ): String = 
{
	val delimLen = if(delimiters == null){-1}else{delimiters.length};
	if (str == null || str.length() == 0 || delimLen == 0) {
		return str;
	}
	val strLen = str.length();
	val buffer = new java.lang.StringBuffer( strLen );
	var capitalizeNext = true;
	for (i <- 0 until strLen) {
		val ch = str.charAt( i );
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
