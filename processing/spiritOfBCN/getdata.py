import random

perc2015 = []
perc2016 = []
perc2017 = []
perc2018 = []
perc2019 = []

def getColor(pais):
	foundColor = 0
	theColor = 0x000000
	for elem in perc2015:
		if elem[0]==pais:
			theColor = elem[2]
			foundColor = 1
	for elem in perc2016:
		if elem[0]==pais:
			theColor = elem[2]
			foundColor = 1
	for elem in perc2017:
		if elem[0]==pais:
			theColor = elem[2]
			foundColor = 1
	for elem in perc2018:
		if elem[2]==pais:
			theColor = elem[2]
			foundColor = 1
	for elem in perc2019:
		if elem[2]==pais:
			theColor = elem[2]
			foundColor = 1
	if foundColor == 0:
		theColor = "%06x" % random.randint(0, 0xFFFFFF)
	return theColor
		
		
	
total = 0

with open('2015_naixements_lloc-de-naixement.csv') as data:
	for line in data:
		fields = line.split(",")
		#print(line)
		#print(fields[len(fields)-1],fields[len(fields)-2])
		found = 0
		total = total + int(fields[len(fields)-1])
		for elem in perc2015:
			if elem[0] == fields[len(fields)-2].replace('"',''):
				elem[1] = elem[1] + int(fields[len(fields)-1])
				found = 1
		if found == 0:
			color = getColor(fields[len(fields)-2].replace('"',''))
			perc2015.append([fields[len(fields)-2].replace('"',''),int(fields[len(fields)-1]),color])
			
total = 0

with open('2016_naixements_lloc-de-naixement.csv') as data:
	for line in data:
		fields = line.split(",")
		#print(line)
		#print(fields[len(fields)-1],fields[len(fields)-2])
		found = 0
		total = total + int(fields[len(fields)-1])
		for elem in perc2016:
			if elem[0] == fields[len(fields)-2].replace('"',''):
				elem[1] = elem[1] + int(fields[len(fields)-1])
				found = 1
		if found == 0:
			color = getColor(fields[len(fields)-2].replace('"',''))
			perc2016.append([fields[len(fields)-2].replace('"',''),int(fields[len(fields)-1]),color])

total = 0

with open('2017_naixements_lloc-de-naixement.csv') as data:
	for line in data:
		fields = line.split(",")
		#print(line)
		#print(fields[len(fields)-1],fields[len(fields)-2])
		found = 0
		total = total + int(fields[len(fields)-1])
		for elem in perc2017:
			if elem[0] == fields[len(fields)-2].replace('"',''):
				elem[1] = elem[1] + int(fields[len(fields)-1])
				found = 1
		if found == 0:
			color = getColor(fields[len(fields)-2].replace('"',''))
			perc2017.append([fields[len(fields)-2].replace('"',''),int(fields[len(fields)-1]),color])

total = 0

with open('2018_naixements_lloc-de-naixement.csv') as data:
	for line in data:
		fields = line.split(",")
		#print(line)
		#print(fields[len(fields)-1],fields[len(fields)-2])
		found = 0
		total = total + int(fields[len(fields)-1])
		for elem in perc2018:
			if elem[0] == fields[len(fields)-2].replace('"',''):
				elem[1] = elem[1] + int(fields[len(fields)-1])
				found = 1
		if found == 0:
			color = getColor(fields[len(fields)-2].replace('"',''))
			perc2018.append([fields[len(fields)-2].replace('"',''),int(fields[len(fields)-1]),color])

total = 0

with open('2019_naixements_lloc-de-naixement.csv') as data:
	for line in data:
		fields = line.split(",")
		#print(line)
		#print(fields[len(fields)-1],fields[len(fields)-2])
		found = 0
		total = total + int(fields[len(fields)-1])
		for elem in perc2019:
			if elem[0] == fields[len(fields)-2].replace('"',''):
				elem[1] = elem[1] + int(fields[len(fields)-1])
				found = 1
		if found == 0:
			color = getColor(fields[len(fields)-2].replace('"',''))
			perc2019.append([fields[len(fields)-2].replace('"',''),int(fields[len(fields)-1]),color])
			
#print(perc2015)

with open("dataOutput2015.csv", "w") as data:
	for elem in perc2015:
		print(elem[0],elem[1],elem[2],total)
		data.write("2015,"+elem[0]+","+str((float(elem[1])/float(total))*100.0)+","+elem[2]+"\n")
		
with open("dataOutput2016.csv", "w") as data:
	for elem in perc2016:
		print(elem[0],elem[1],elem[2],total)
		data.write("2016,"+elem[0]+","+str((float(elem[1])/float(total))*100.0)+","+elem[2]+"\n")
		
with open("dataOutput2017.csv", "w") as data:
	for elem in perc2017:
		print(elem[0],elem[1],elem[2],total)
		data.write("2017,"+elem[0]+","+str((float(elem[1])/float(total))*100.0)+","+elem[2]+"\n")
		
with open("dataOutput2018.csv", "w") as data:
	for elem in perc2018:
		print(elem[0],elem[1],elem[2],total)
		data.write("2018,"+elem[0]+","+str((float(elem[1])/float(total))*100.0)+","+elem[2]+"\n")
		
with open("dataOutput2019.csv", "w") as data:
	for elem in perc2019:
		print(elem[0],elem[1],elem[2],total)
		data.write("2019,"+elem[0]+","+str((float(elem[1])/float(total))*100.0)+","+elem[2]+"\n")
