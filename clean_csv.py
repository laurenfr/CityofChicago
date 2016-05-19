import csv

def clean_csv(filename, cutby):
	# filename is string of filename in same directory
	# cutby is the column that will be used for cutting
	original = open(filename, "rU")
	read_original = csv.reader(original)
	new = []
	new_file_name = 'cutfile.csv'
	new_file = open(new_file_name, 'w')
	wr_new_file = csv.writer(new_file, dialect = 'excel')
	for row in read_original:
		# loops through rows of file
		new_row = row
		# make room for new column
		new_row.append('')
		if new_row[8] == 'location':
			new_row[8] = 'latitude'
			new_row[9]= 'longitude'
		if '#' in new_row[1]:
			new_row[1] = new_row[1].replace("#", "No. ")
		if '#' in new_row[2]:
			new_row[2] = new_row[2].replace("#", "No. ")
		# separates coordinates into longitude and latitude
		coordinates = new_row[8].split(',')
		for coordinate in coordinates:
			if '(' in coordinate:
				new_row[8] = coordinate.replace('(','')
			elif ')' in coordinate:
				new_row[9] = coordinate.replace(')','')
		entry = str(row[cutby])
		splitting = entry.split(',')
		count = len(splitting)-1
		# checks column to see if it has multiple entries
		while count >= 0:
			if ' ' in splitting[count]:
				splitting[count] = splitting[count].replace(' ', '')
			new_row[cutby] = splitting[count]
			wr_new_file.writerow(new_row)
			count -= 1
		# until entries < 0, creates copy of row with split entries
	new_file.close()
	del new_file
	del wr_new_file

clean_csv('CTA_-_Ridership_-_Avg._Weekday_Bus_Stop_Boardings_in_October_2012.csv'\
			,3)