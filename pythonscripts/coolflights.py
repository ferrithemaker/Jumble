import urllib
import sys
from bs4 import BeautifulSoup

# llegim llista notcool

def notcool():
	with open("notcool") as f:
    		content = f.readlines()
	return [x.strip() for x in content]

def destins(direccio):
	llista_destins = []
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=0"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	destins = linea_vol.findAll("div", {"id": "fdest"})
        	for desti in destins:
                	llista_destins.append(desti.text.strip())
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=6"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	destins = linea_vol.findAll("div", {"id": "fdest"})
        	for desti in destins:
                	llista_destins.append(desti.text.strip())
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=12"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	destins = linea_vol.findAll("div", {"id": "fdest"})
        	for desti in destins:
                	llista_destins.append(desti.text.strip())
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=18"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	destins = linea_vol.findAll("div", {"id": "fdest"})
        	for desti in destins:
                	llista_destins.append(desti.text.strip())
	return llista_destins

def hores(direccio):
	llista_hores = []
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=0"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	hores = linea_vol.findAll("div", {"id": "fhour"})
        	for hora in hores:
                	llista_hores.append(hora.text.strip())
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=6"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	hores = linea_vol.findAll("div", {"id": "fhour"})
        	for hora in hores:
                	llista_hores.append(hora.text.strip())
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=12"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	hores = linea_vol.findAll("div", {"id": "fhour"})
        	for hora in hores:
                	llista_hores.append(hora.text.strip())
	url = "http://www.barcelona-airport.com/cat/"+direccio+".php?tp=18"
	sock = urllib.urlopen(url)
	pagina = BeautifulSoup(sock.read(), "lxml")
	linies_vol = pagina.findAll("div", {"id": "flight_detail"})
	for linea_vol in linies_vol:
        	hores = linea_vol.findAll("div", {"id": "fhour"})
        	for hora in hores:
                	llista_hores.append(hora.text.strip())
	return llista_hores




if len(sys.argv) == 2 and (sys.argv[1] == "arribades" or sys.argv[1] == "sortides"):

	notcool = notcool()
	if sys.argv[1] == "arribades":
		llista_destins_arribades = destins("arribades")
	        llista_hores_arribades = hores("arribades")
		index = 0
		elementprevi = ""
		print "ARRIBADES"
		if len(llista_destins_arribades) == len(llista_hores_arribades):
			while index<len(llista_destins_arribades):
				elementactual=llista_destins_arribades[index]+" "+llista_hores_arribades[index]
				destiactual=llista_destins_arribades[index]
				if elementprevi!=elementactual and destiactual not in notcool:
					print elementactual
				elementprevi = elementactual
				index = index + 1


	if sys.argv[1] == "sortides":
		llista_destins_sortides = destins("sortides")
	        llista_hores_sortides = hores("sortides")
		index = 0
		elementprevi = ""
		print "SORTIDES"
		if len(llista_destins_sortides) == len(llista_hores_sortides):
        		while index<len(llista_destins_sortides):
                		elementactual=llista_destins_sortides[index]+" "+llista_hores_sortides[index]
                		destiactual=llista_destins_sortides[index]
                		if elementprevi!=elementactual and destiactual not in notcool:
                        		print elementactual
                		elementprevi = elementactual
                		index = index + 1


else:
	print "Us: python coolflights.py [arribades] [sortides]"
