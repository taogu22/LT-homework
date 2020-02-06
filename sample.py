from itertools import islice

# Open all 3 files.
bmFile = open("bm-value.txt", "r")
yearBeginFile = open("year-begin.txt", "r")
yearEndFile = open("year-end.txt", "r")
dpsFile = open("dps.txt", "r")
testFile = open("test.txt", "r")

bmList, yearBeginList, yearEndList, dpsList = [], [], [], []
testList = []
# For bm-value.txt
# Iterate all lines starting from the second line.
for line in islice(bmFile, 1, None):
	# Create a list for every line, each representing one single id.
	lineList = []
	# print(line)
	for word in line.split():
		lineList.append(float(word))
	bmList.append(lineList)

# For year-begin.txt
for line in islice(yearBeginFile, 1, None): # Start from second line.
	# Create a list for every line, each representing one single id.
	lineList = []
	# print(line)
	for word in line.split():
		lineList.append(float(word))
	yearBeginList.append(lineList)

# For year-end.txt
for line in islice(yearEndFile, 1, None): # Start from second line.
	# Create a list for every line, each representing one single id.
	lineList = []
	# print(line)
	for word in line.split():
		lineList.append(float(word))
	yearEndList.append(lineList)

# For dps.txt
for line in islice(dpsFile, 1, None): # Start from second line.
	# Create a list for every line, each representing one single id.
	lineList = []
	# print(line)
	for word in line.split():
		lineList.append(float(word))
	dpsList.append(lineList)

# Fill in the above lists, such that empty years have value 0.
def fillList(myList):
    numStock = len(myList)
    numYear = 21
    newList = []
    for stock in range(0, numStock):
        curList = myList[stock][1:] # delete the first element (year) from the stock list
        for i in range(0, numYear - len(curList)): # if there is empty year, then add value 0 for this year.
            curList.insert(0, 0)
        newList.append(curList)
    return newList
        

# Transpose the list of lists
def transpose(myList):
    fstNum = len(myList)
    sndNum = len(myList[0])
    newList = []
    for j in range(0, sndNum):
        newElem = []
        for i in range(0, fstNum):
            newElem.append(myList[i][j])
        newList.append(newElem)
    return newList

# Make 5 groups of stokcs according to the value, and put the remainder in the middle (3rd) group.
# Input is a list of values, whose indexes are id of stocks. We first filter out those stocks with value 0.
def grouping(myList):
    listSize = len(myList)
    count = sum(map(lambda x : x > 0, myList)) # number of stocks of that year
    groupSize = count // 5
    remainder = count % 5
    ordering = sorted(range(listSize) , key = lambda i : myList[i])
    ordering = ordering[listSize - count : ] # ordering of indexes with nonzero values.
    # return(len(ordering) == count)
    group = [ordering[0 : groupSize], ordering[groupSize : groupSize*2], ordering[groupSize * 2 : groupSize * 3 + remainder], ordering[groupSize * 3 + remainder : groupSize * 4 + remainder], ordering[groupSize * 4 + remainder : ]]    # group = [] # maintain a list whose 5 elements are lists of the indexes of the stocks in the corresponding group.
    group.reverse()
    return group

# listS = transpose(fillList(bmList))[0]

bmFList, yearBeginFList, yearEndFList, dpsFList = fillList(bmList), fillList(yearBeginList), fillList(yearEndList), fillList(dpsList)
bmTList, yearBeginTList, yearEndTList, dpsTList = transpose(bmFList), transpose(yearBeginFList), transpose(yearEndFList), transpose(dpsFList)

def decideGroup(dataType, year): # input dataType is the original data of bm values
    # decide the grouping according to the given datatype and year
    index = year - 1998 # Years for bm-values start from 1998
    data = transpose(fillList(dataType))
    group = grouping(data[index])
    return group

# dps of num-many stock for the corresponding year
#def dpsYear(stock, year, num):
#    index = year - 1998 # dps year starts from 1998 (in 1998 they are all 0)
#    return dpsTList[index][stock] * num

# return a list of floats, each is how many stocks one buys
def stockBuy(stockList, year, funds):
    count = len(stockList)
    fundsEach = funds / count
    curYearPrice = yearBeginTList[year - 1999] # year for begin-values starts from 1999
    return list(map(lambda i : fundsEach / curYearPrice[i] ,stockList))

def dps(stock, yearStart, yearEnd, stockCount):
    stockDpsList = dpsFList[stock][yearStart - 1998 : yearEnd - 1998 + 1]
    dpsTotal = sum(stockDpsList)
    return dpsTotal * stockCount
    

# return a list of profits
def dpsForList(stockList, yearStart, yearEnd, stockCountList):
    listL = []
    for i in range(0, len(stockList)):
        listL.append(dps(stockList[i], yearStart, yearEnd, stockCountList[i]))
    return listL
    
# for a single year
def dpsYear(stock, year, stockCount):
    return dps(stock, year, year, stockCount)
    

# return a list of profits, for a single yaer
def dpsForListYear(stockList, year, stockCountList):
    return dpsForList(stockList, year, year, stockCountList)

# buy and hold: 20 years
initGroup = decideGroup(bmList, 1998)
initFunds = 100
initBuy = [] # list of how many stock initially
for i in range(0, 5):
    l = stockBuy(initGroup[i], 1999, initFunds)
    initBuy.append(l)
# for year in range(1999, 2018 + 1):

myYear = 1999
dpsList = []
for i in range(0, 5):
    stockList = initGroup[i]
    stockCountList = initBuy[i]
    dpsSum = sum(dpsForListYear(stockList, myYear, stockCountList))
    dpsList.append(dpsSum)

# bmYear is used to decide how to make the groups
# initFunds is the funds at initYear for each group
def buyHold(bmYear, initFundsList, curYear):
    initGroup = decideGroup(bmList, bmYear) # grouping determined by bm-value on the initial year, from high to low
    initBuy = [] # # a list keeping track of how many stocks one buys
    for i in range(0, 5):
        l = stockBuy(initGroup[i], bmYear + 1, initFundsList[i]) # the price one buys the stocks is the next year of bmYear, so use bmYear + 1.
        initBuy.append(l)
    dpsList = []
    for i in range(0, 5):
        stockList = initGroup[i]
        stockCountList = initBuy[i]
        dpsSum = sum(dpsForListYear(stockList, curYear, stockCountList))
        dpsList.append(dpsSum)
    return dpsList


# Example: buy-and-hold for 20 years
bmYear = 1998
initFunds = 1000000
initFundsList = [1000000, 1000000, 1000000, 1000000, 1000000]
myList = []
for curYear in range(1999, 2018 + 1):
    myList.append(buyHold(bmYear, initFundsList, curYear))
    

'''
def rebalance(startYear, endYear, initFunds):
    funds = initFunds
    dpsList = []
    for year in range(startYear, endYear + 1):
        initGroup = decideGroup(bmList, year - 1) # first decide grouping according to bm-values of last year
        
'''






