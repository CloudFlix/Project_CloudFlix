f = open("/Users/pratiksomanagoudar/Desktop/test.csv", "r" )
f1= open("/Users/pratiksomanagoudar/Desktop/test_new.csv" , "w+")
parts = []
lines= f.readlines()
for line in lines:
	print("running")
	part=line.split(",")
	val = int(part[0])
	if val in parts:
		x=1
	else:
		parts.append(val)

for word in parts:
	f1.write(str(word)+"\n")
