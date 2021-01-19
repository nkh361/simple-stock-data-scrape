from bs4 import BeautifulSoup
import urllib3
import webbrowser

def get_Symbol_Link():
	symbol = input("Enter a NYSE symbol: ")
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
		print("Current price: $", current)

	tableElements=[]

	for tp in targetPrice:
		target = tp.string
		tableElements.append(target)

	if len(tableElements) <= 0:
		print("No target price data available")
	else:		
		print('Average target price: $', tableElements[1])


def main():
	get_Current_Stats()

main()