class add_jodatime {
public final int iMax = 12;
public long add( long instant, int months )
{
	if (months == 0) {
		return instant;
	}
	long timePart = 1516149603588L; //iChronology.getMillisOfDay( instant );
	int thisYear = 2018; //iChronology.getYear( instant );
	int thisMonth = 0; //iChronology.getMonthOfYear( instant, thisYear );
	int yearToUse;
	int monthToUse = thisMonth - 1 + months;
	if (monthToUse >= 0) {
		yearToUse = thisYear + monthToUse / iMax;
		monthToUse = monthToUse % iMax + 1;
	} else {
		yearToUse = thisYear + monthToUse / iMax - 1;
		monthToUse = Math.abs( -monthToUse );
		int remMonthToUse = monthToUse % iMax;
		if (remMonthToUse == 0) {
			remMonthToUse = iMax;
		}
		monthToUse = iMax - remMonthToUse + 1;
		if (monthToUse == 1) {
			yearToUse += 1;
		}
	}
	int dayToUse = 16; /* iChronology.getDayOfMonth( instant, thisYear, thisMonth ); */
	int maxDay = 31; /* iChronology.getDaysInYearMonth( yearToUse, monthToUse ); */
	if (dayToUse > maxDay) {
		dayToUse = maxDay;
	}
	/*long datePart = iChronology.getYearMonthDayMillis( yearToUse, monthToUse, dayToUse );
	  return datePart + timePart; */
	return yearToUse + monthToUse + dayToUse + timePart; //not a real time but ok
}
}
