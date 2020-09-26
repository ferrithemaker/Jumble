perc = []
total = 0
year = "2015"

with open('2015_naixements_lloc-de-naixement.csv') as data:
	for line in data:
		fields = line.split(",")
		#print(line)
		#print(fields[len(fields)-1],fields[len(fields)-2])
		found = 0
		total = total + int(fields[len(fields)-1])
		for elem in perc:
			if elem[0] == fields[len(fields)-2].replace('"',''):
				elem[1] = elem[1] + int(fields[len(fields)-1])
				found = 1
		if found == 0:
			perc.append([fields[len(fields)-2].replace('"',''),int(fields[len(fields)-1])])
			
print(perc)
with open("dataOutput2015.csv", "w") as data:
	for elem in perc:
		print(elem[0],elem[1],total)
		data.write(year+","+elem[0]+","+str((float(elem[1])/float(total))*100.0)+"\n")
