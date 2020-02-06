from itertools import islice

##################
''' 
只需要更改下面一小段的代码
运行代码时，将需要运行的部分前面的井号#去掉。同样的，不需要执行某一部分代码时可以在改行前加上井号#。
需要执行的是 print() 的行。
'''

# buy and hold
''' 
函数buyAndHold(bmYear, initFundsList, endYear)有三个变量. 
1. bmYear = 用以决定分组的年份，例如：1998
2. initFundLists = 每一组一开始的启动资金，例如：[1000000, 1000000, 1000000, 1000000, 1000000] （也可以写作[1000000] * 5）
3, endYear = 该跨度结束的年份，例如：2000
The function outputs a list on length 5, whose elements are the profits of the group at the current year.
'''

# example: 20年跨度 1999-2018
# print(buyAndHold(1998, [1000000] * 5, 2018))
# example: 10年跨度,共有两个跨度分别为1999-2008和2009-2018
# print(buyAndHold(1998, [1000000] * 5, 2008))
# print(buyAndHold(2008, [1000000] * 5, 2018))


# rebalance
'''
函数rebalance(startYear, endYear, initFunds)也有三个变量：
1.startyear是跨度开始的年份，例如1999
2.endYear是跨度结束的年份，例如2018
3.initFunds依然是跨度一开始每一组的启动资金，例如：[1000000] * 5
'''
# example：20年跨度
print(rebalance(1999, 2018, [1000000]*5))
##################








'''请不要修改以下内容'''

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

# return the funds earned by selling a stock at the given year
def stockSell(stock, count, year):
    price = yearEndFList[stock][year - 2000] # sell price is that at the end of last year
    return count * price

# return the funds earned by selling a list of stocks for a list of prices at the given year
def stockSellList(stockList, countList, year):
    funds = 0
    for i in range(0, len(stockList)):
        funds += stockSell(stockList[i], countList[i], year)
    return funds

# return a list of stocks to sell:
def stockToSell(oldStocks, newStocks):
    myList = []
    for stock in oldStocks:
        if stock not in newStocks:
            myList.append(stock)
    return myList

# return a list of stocks to buy:
def stockToBuy(oldStocks, newStocks):
    myList = []
    for stock in newStocks:
        if stock not in oldStocks:
            myList.append(stock)
    return myList

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

def buyAndHold(bmYear, initFundsList, endYear):
    myList = []
    for year in range(bmYear + 1, endYear + 1):
        profit = buyHold(bmYear, initFundsList, year)
        myList.append(profit)
    return myList


# Example: buy-and-hold for 20 years
bmYear = 1998
initFunds = 1000000
initFundsList = [1000000] * 5
myList = []
for curYear in range(1999, 2018 + 1):
    myList.append(buyHold(bmYear, initFundsList, curYear))
initAmountList = [0] * len(bmList) # initially no stock

# modify amountList
def buyStock(stockList, year, funds, amountList):
    fundsEach = funds / len(stockList) # the funds for each stock in stockList
    for stock in stockList:
        price = yearBeginFList[stock][year - 1999] # year for begin-values starts from 1999
        newAmount = fundsEach / price
        amountList[stock] = newAmount
    return amountList

# 
def groupStockToSell(oldGroup, newGroup):
    myList = []
    for i in range(0,len(oldGroup)):
        myList.append(stockToSell(oldGroup[i], newGroup[i]))
    return myList

def groupStockToBuy(oldGroup, newGroup):
    myList = []
    for i in range(0,len(oldGroup)):
        myList.append(stockToBuy(oldGroup[i], newGroup[i]))
    return myList

# return [funds, funds, ..., funds], each stands for the funds in that group after selling the stocks
def groupFunds(oldGroup, newGroup, year, amountList):
    myList = []
    sellGroup = groupStockToSell(oldGroup, newGroup)
    for group in sellGroup:
        funds = 0
        for stock in group:
            amount = amountList[stock]
            price = yearEndFList[stock][year - 2000] # The selling price is the price at the end of last year, and year-end price starts from 1999. 
            funds += amount * price
        myList.append(funds)
    return myList

# modify the amountList based on the group change
def updateAmountList(groupToBuy, fundsForGroup, amountList, year):
    amount = amountList
    for group in range(0, len(groupToBuy)):
        amount = buyStock(groupToBuy[group], year, fundsForGroup[group], amount)
    return amount

# return a list of dps for each group in that year
def calDps(grouping, amountList, year):
    myList = []
    for group in range(0, len(grouping)):
        earn = 0
        for stock in grouping[group]:
            amount = amountList[stock]
            stockDps = dpsFList[stock][year - 1998] # dps has 0 in the front for year 1998
            earn += amount * stockDps
        myList.append(earn)
    return myList

# rebalance
def rebalance(startYear, endYear, initFundsList):
    funds = initFundsList # initially every group has the same funds 
    dpsList = [] # the list of the dps of all 5 groups
    amountList = [0] * len(bmList) # initially no stock
    oldGrouping = [[]] * 5 # initially no stock
    for year in range(startYear, endYear + 1):
        newGrouping = decideGroup(bmList, year - 1) # first decide grouping according to bm-values of last year
        groupToBuy = groupStockToBuy(oldGrouping, newGrouping)
        nextYearFunds = groupFunds(oldGrouping, newGrouping, year, amountList)
        amountList = updateAmountList(groupToBuy, funds, amountList, year) # modify amountList
        funds = nextYearFunds
        dpsList.append(calDps(newGrouping, amountList, year))
        oldGrouping = newGrouping
    return dpsList








