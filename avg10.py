def readData(filename):
	#open file, read file, put into new string of array when split

	#1. open the file and read ALL LINES into arrLines
	#about 3 lines of code

	f2 = open(filename, "r");
	arrLines= f2.readlines();
	f2.close();

	#2. declare empty array: arrRet
	arrRet=[];

	#3. declare variable idxLine, intiialize to last index
	idxLine=len(arrLines)-1;

	#4. WHILE LOOP: idxLine ---> 1: (0 not included!why?..so we can skip the letters)

	while idxLine >=1:
		arrData=arrLines[idxLine].split(",");
		sDate=arrData[0]
		fOpen=float(arrData[1]);
		arrRecord= [sDate, fOpen];
		arrRet.append(arrRecord);
		idxLine -=1;
	return arrRet

	#____________________________________________________________
print(readData("GOOG.csv"));

def get10DayAvg(data, i):
	isum=0;
	#at day 0, cant compute the previous 10 days if there arent any previous days
	if i==0:
		return data[0][1]

	elif i < 10:
		c = 0;
		maxIdx = i - 1;
		while c <= maxIdx:
			isum += data[c][1];
			c+=1;

	else:
		c=0;
		#idx to sort through
		idx=i-1;

		while idx >=0 and c <10:
			#2d array, idx-c is the sorting component. the [1] is the opening value at the specific idx
			isum+=data[idx-c][1];
			c+=1;
	avg  = isum/c
	return avg;

data = readData("GOOG.csv")
avgLast = get10DayAvg(data, len(data)-1);
print("10-day avg for the last day is: " + str(avgLast));

def backtest(data, perc, initFund):

	fcash = initFund;
	ishares= 0.0;
	c = 0;
	last= data[len(data)-1][1];
#	idx=data[c][1];

	#loop through array: from 0,251
	while c >= 0 and c<= len(data)-1:

		tenDayAvgPrice = get10DayAvg(data,c);
		price = data[c][1];
		buyPrice = (1 - (perc/100)) * tenDayAvgPrice;
		sellPrice = (1 + (perc/100)) * tenDayAvgPrice;

		if price < buyPrice:
			cash = fcash;
			fcash = fcash % price;
			ishares += cash // price;

		elif price > sellPrice:
			fcash += ishares * price;
			ishares = 0;

		c+=1;
	return fcash + ishares * last;

data = readData("GOOG.csv");
initFund = 10000.0;
total = backtest(data, 1.0, initFund);
profit = (total - initFund) / (initFund) * 100.0;
print("profit is: " + str(profit) + "%");


def modOptimization():
	data = readData("GOOG.csv");
	initFund = 10000.0;
	c=0;
	global x;
	x = 0;
	max = backtest(data, 0.1, initFund);
	while c <= 10:
		if backtest(data, c, initFund) > max:
			max = backtest(data, c, initFund);

		c+=.1;

	while x <= 10:
		if max == backtest(data, x, initFund):
			break;
		x += 0.1;

	profit = (max - initFund) / (initFund) * 100.0;
	return profit

operation = modOptimization()
print("max profit is: " + str(operation) + ", at perc: " + str(x))
