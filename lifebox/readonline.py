from bs4 import BeautifulSoup
import urllib3
import time

http = urllib3.PoolManager()

url = 'http://lifebox.ferranfabregas.me/lifeboxdata'

pinArray = [512,512,512,512,512,512,512,512,512,512,512]

while(True):
	time.sleep(2)
	datafromurl = http.request('GET', url)
	soup = BeautifulSoup(datafromurl.data,'lxml')
	for p in soup.find_all('p'):
		p=str(p).replace('<p>','').replace('</p>','').split('|')
		index = 0
		for data in p:
			#print(data)
			pinArray[index] = int(data)
			index = index + 1
	f = open('controllerdata','w')
	for element in pinArray:
		f.write(str(element))
		f.write('\n')
	f.close()
