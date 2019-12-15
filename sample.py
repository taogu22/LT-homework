from itertools import islice

# Open all 3 files.
bmFile = open("bm-value.txt", "r")
yearBeginFile = open("year-begin.txt", "r")
yearEndFile = open("year-end.txt", "r")
testFile = open("test.txt", "r")

bmList, yearBeginList, yearEndList = [], [], []
testList = []
# For bm-value.txt
# Iterate all lines starting from the second line.
for line in islice(bmFile, 1, None):
	# Create a list for every line, standing for one single id.
	lineList = []
	print(line)
	for word in line.split():
		lineList.append(word)
	bmList.append(lineList)

# For year-begin.txt
for line in islice(yearBeginFile, 1, None): # Start from second line.
	# Create a list for every line, standing for one single id.
	lineList = []
	print(line)
	for word in line.split():
		lineList.append(word)
	yearBeginList.append(lineList)

# For year-end.txt
for line in islice(yearEndFile, 1, None): # Start from second line.
	# Create a list for every line, standing for one single id.
	lineList = []
	print(line)
	for word in line.split():
		lineList.append(word)
	yearEndList.append(lineList)