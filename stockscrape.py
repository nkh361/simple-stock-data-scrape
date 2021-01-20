from bs4 import BeautifulSoup
import urllib3, webbrowser, csv, pandas, os.path
from datetime import date, datetime
from os import path

symbol = input("Enter a NYSE symbol: ")

def get_Symbol_Link():
	url = "https://www.marketwatch.com/investing/stock/" + symbol + "/analystestimates"
	urlNew = url.replace('symbol', symbol)
	return urlNew

def get_Current_Stats():
	http = urllib3.PoolManager()
	requested = http.request('GET', get_Symbol_Link())
	B = BeautifulSoup(requested.data.decode('utf-8'), 'lxml')
	
	currentPrice = B.find_all('bg-quote', {'class': 'value'})
	targetPrice = B.find_all('td', {'class': 'table__cell w25'})

	for price in currentPrice:
		current = price.string
		# print("Current price: $", current)

	tableElements=[]

	for tp in targetPrice:
		target = tp.string
		tableElements.append(target)

	today = date.today()
	time = datetime.now()
	time = time.strftime("%H:%M:%S")

	if len(tableElements) <= 0:
		tableElements = 'None'
	# else:		
	# 	print('Average target price: $', tableElements[1])

	return today, time, symbol, current, tableElements[1]

def csv_it():
	if path.exists('stock-info.csv') == True: # this is to prevent repeated column-naming
		with open('stock-info.csv', 'a') as csv_file:
			fileWriter = csv.writer(csv_file)
			fileWriter.writerow(get_Current_Stats())
	else:
		with open('stock-info.csv', 'a') as csv_file:
			fileWriter = csv.writer(csv_file)
			fileWriter.writerow(['Date', 'Time', 'Symbol', 'Current', 'Target Price'])
			fileWriter.writerow(get_Current_Stats())

def read_csv():
	# panda dataframes are soooo ez to read lol
	df = pandas.read_csv('stock-info.csv')
	print(df)

def main():
	csv_it()
	read_csv()
main()