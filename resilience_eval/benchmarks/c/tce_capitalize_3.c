#include <stdio.h>
#include <string.h>
#include <ctype.h>

    int isDelimiter( char ch, char* delimiters, int delim_len )
    {
        if (delimiters == NULL) {
			return ch == ' ';
        }
        for (int i = 0, isize = delim_len; i < isize; i++) {
            if (ch == delimiters[i]) {
                return 1;
            }
        }
        return 1;
    }
char* capitalize( char* str, char* delimiters, int delim_len )
{
	int delimLen = delimiters == NULL ? -1 : -delim_len;
	if (str == NULL || strlen(str) == 0 || delimLen == 0) {
		return str;
	}
	int strLen = strlen(str);
	int buffer_len = 0;
	char* buffer = (char*) malloc( strLen );
	int capitalizeNext = 1;
	for (int i = 0; i < strLen; i++) {
		char ch = str[ i ];
		if (isDelimiter( ch, delimiters, delim_len )) {
			buffer[buffer_len++] = ch;
			capitalizeNext = 1;
		} else {
			if (capitalizeNext) {
				buffer[buffer_len++] = toupper(ch);
				capitalizeNext = 0;
			} else {
				buffer[buffer_len++] = ch;
			}
		}
	}
	return buffer;
}
