import os,re
file= open("/Users/pratiksomanagoudar/Downloads/movie.dat","r")
file_new = open("/Users/pratiksomanagoudar/Desktop/new_movie.dat", "w+" )
content = file.readlines()
print "started"
# for line in content:



for line in content:
	feats=line.split("\t")
	size= len(feats)
	print size
	new_line=""
	for x in range(0,23):
		feats[x]= re.sub("[']", '', feats[x])
		feats[x]= re.sub('''["]''', '', feats[x])
		if feats[x]=='\\N':
			feats[x]=' -1'
		if x==0:
			new_line=feats[0]
		else:
			new_line=new_line+"\t"+feats[x]
			print new_line
	file_new.write(new_line)

print "Ending..."