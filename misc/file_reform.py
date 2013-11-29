
import os,re

for dirname, dirnames, filenames in os.walk('/Users/pratiksomanagoudar/Downloads/30sets'):
    for filename in filenames:
        print filename
        new_file_name =  filename
        new_path_name =  dirname+"_new"
        file_new = open(new_path_name+"/"+new_file_name, "w+" )
        with open(dirname+"/"+filename) as f:
            content = f.readlines()
            i=0
            for line in content:
                if i==0:
                    i=i+1
                    n_line=re.sub("Class", ',Class', line)
                    file_new.write(n_line)
                    continue

                line_new=""
                flag='f'
                feats=line.split(",")
                
                if len(feats)>39:
                    flag='t'
                for x in range(0, 39):
                    feats[x]= re.sub("[']", '', feats[x])
                    feats[x]= re.sub('''["]''', '', feats[x])
                    if feats[x]==' \\N':
                        feats[x]=' -1'
                    if x==0:
                        line_new=feats[x]
                    else:   
                        line_new=line_new+","+feats[x]
                if flag=='t':
                    line_new=line_new+"\n"
                    flag=='f'
                file_new.write(line_new)

