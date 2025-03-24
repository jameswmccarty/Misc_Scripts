"""
Run queries on SVM based on PERSTEMPO history

Will project meeting 220/400 day waiver limits based
on an Alpha report from the PERSTEMPO system and
projected deployment dates.
"""

# https://docs.python.org/3/library/datetime.html
from datetime import date, timedelta

# lines not useful in the report
discards = ["(FOUO)", "_", "LST4", "CUMULATIVE DAY WINDOW", "LAST DAY", "ALPHA LISTING", "BSO:", "DISTRIBUTION", "TTL", "WEEKLY", "REPORT AS OF"]

# countable category codes (including all A-E)
valid_codes = ['A','B','C','D','E']

# sanitized input
raw_records = []

# container for SVM records
svm = dict()

"""
take a date in format "03-SEP-19" and return a date
object.  If string is blank, return today's date.
"""
def convert_date(date_str):
	# index months 1 - 12
	months = [None,"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
	if date_str == '':
		return date.today()
	d, m, y = date_str.split("-")
	if len(y) == 2: # convert to 4 digit year
		y = '20' + y
	return date(int(y),months.index(m.upper()),int(d))

"""
return all days between a starting and ending date for a SVM
"""
def count_window(svm_name, start_date, curr_event_start_date, end_date):
	counter = 0
	if end_date < start_date:
		print("Error: Starting date is after the end date.  Cannot continue.")
		exit()
	anchor_date = start_date
	while anchor_date < end_date:
		# in the window of a past event
		for event in svm[svm_name]:
			if anchor_date >= event[0] and anchor_date <= event[1]:
				counter += 1
		# in the window of the current event
		if anchor_date >= curr_event_start_date:
			counter += 1
		anchor_date += timedelta(days=1)
	return counter

"""
Run a forecast for a PERSTEMPO event
Notify which dates SVM will trip 220 or 400
Threshold dates, and display final counter
at end of projected trip.
"""
def run_query(svm_name, start_date, end_date):
	one_day = timedelta(days=1)
	over_220 = False
	over_400 = False
	anchor_date = start_date
	while anchor_date < end_date:
		count365 = count_window(svm_name, anchor_date - 365*one_day, start_date, anchor_date)
		if count365 > 220 and not over_220:
			print("SVM exceeds 220 days on ", anchor_date)
			over_220 = True
		count730 = count_window(svm_name, anchor_date - 730*one_day, start_date, anchor_date)
		if count730 > 400 and not over_400:
			print("SVM exceeds 400 days on ", anchor_date)
			over_400 = True
		anchor_date += one_day
	count365 = count_window(svm_name, end_date - 365*one_day, start_date, end_date)
	count730 = count_window(svm_name, end_date - 730*one_day, start_date, end_date)
	print("Final 365 day count at end of event will be ", count365)
	print("Final 730 day count at end of event will be ", count730)

if __name__ == "__main__":

	# Clean input to only the lines with data entries
	with open("PERSTEMPO_TEXT.txt", "r") as infile:
		for line in infile.readlines():
			if line.strip() != '' and len([_ for _ in discards if _ in line])==0:
					raw_records.append(line.strip())

	# parse out valid event dates for each person
	for line in raw_records:
		svm_name = line[0:7].strip()+'_'+line[9:14].strip() # last plus last 4 SSN
		start_date = line[26:36].strip()
		end_date   = line[36:46].strip()
		event_category = line[57]
		if start_date != '' and event_category in valid_codes:
			start_date = convert_date(start_date)
			end_date   = convert_date(end_date)
			if svm_name in svm:
				svm[svm_name].append((start_date, end_date))
			else:
				svm[svm_name] = [(start_date, end_date)]

	# display prompt, enter loop
	while True:
		svm_name   = None
		start_date = None
		end_date   = None
		print()
		print("SVMs in data set are: " + ", ".join(list(svm.keys())))
		while svm_name not in svm.keys():
			svm_name = input("Enter name of SVM (e.g. 'SMITH A_2341'): ")
			if svm_name not in svm.keys():
				print("Error: Entry not valid.")
		start_date = input("Enter projected event start date (e.g. '18-Apr-2015'): ")
		end_date   = input("Enter a projected event end date (e.g. '20-May-2015'): ")
		start_date = convert_date(start_date)
		end_date   = convert_date(end_date)
		print()
		print("***History for " + svm_name +":")
		for event in svm[svm_name]:
			print("      ", event[0], event[1], str(event[1]-event[0]).split(", ")[0])
		print(" *new:", start_date, end_date)
		run_query(svm_name, start_date, end_date)