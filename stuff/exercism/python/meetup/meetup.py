import calendar, datetime

class MeetupDayException(Exception):
	pass

dict_weekday = {
	'Monday' : 0,
	'Tuesday' : 1,
	'Wednesday' : 2,
	'Thursday' : 3,
	'Friday' : 4,
	'Saturday' : 5,
	'Sunday' : 6,
}

def meetup_day(year, month, day_of_the_week, which):
    cal = calendar.monthcalendar(year,month)
    if which == 'last':
    	day = find_last(cal,day_of_the_week)
    elif which == 'teenth':
    	day = find_teenth(cal,day_of_the_week)
    else:
    	day = find_num(cal,day_of_the_week,int(which[0]))
    return datetime.date(year,month,day)

def find_last(cal,dotw):
	if cal[len(cal)-1][dict_weekday.get(dotw)] == 0:
		return cal[len(cal)-2][dict_weekday.get(dotw)]
	else:
		return cal[len(cal)-1][dict_weekday.get(dotw)]

def find_teenth(cal,dotw):
	date_sel = []
	for i in range(len(cal)):
		date_sel.append(cal[i][dict_weekday.get(dotw)])
	for i in date_sel:
		if i in range(13,20):
			return i

def find_num(cal,dotw,count):
	date_sel = []
	for i in range(len(cal)):
		date_sel.append(cal[i][dict_weekday.get(dotw)])
	date_sel = filter(lambda date: date != 0,date_sel)
	if count > len(date_sel):
		raise MeetupDayException("Invalid Date!")
	return date_sel[count-1]