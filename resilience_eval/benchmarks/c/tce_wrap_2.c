#include <string>
char LINE_SEPARATOR = '\n';
char* wrap( std::string* str, int wrapLength, char newLineStr, int wrapLongWords )
{
	if (str == NULL) {
		return NULL;
	}
	if (newLineStr == 0) {
		newLineStr = LINE_SEPARATOR;
	}
	if (wrapLength < 1) {
		wrapLength = 1;
	}
	int inputLineLength = str->length();
	int offset = 0;
	std::string wrappedLine;
	wrappedLine.reserve( inputLineLength * 32 );
	while (inputLineLength - offset > wrapLength) {
		if ((*str)[ offset ] == ' ') {
			offset++;
			continue;
		}
		int spaceToWrapAt = str->find_last_of( ' ', wrapLength + offset );
		if (spaceToWrapAt >= offset) {
			wrappedLine.append( str->substr( offset, spaceToWrapAt ) );
			wrappedLine.append( 1, newLineStr );
			offset = spaceToWrapAt + 1;
		} else {
			if (wrapLongWords) {
				wrappedLine.append( str->substr( offset, wrapLength + offset ) );
				wrappedLine.append( 1, newLineStr );
				offset += wrapLength;
			} else {
				spaceToWrapAt = str->find( ' ', wrapLength + offset );
				if (spaceToWrapAt >= 0) {
					wrappedLine.append( str->substr( offset, spaceToWrapAt ) );
					wrappedLine.append( 1, newLineStr );
					offset = spaceToWrapAt + 1;
				} else {
					wrappedLine.append( str->substr( offset ) );
					offset = inputLineLength;
				}
			}
		}
	}
	wrappedLine.append( str->substr( offset ) );
	return (char*) wrappedLine.c_str();
}
