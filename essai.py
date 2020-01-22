import json
import sys
point=".json"

argv ="%s %s" % (sys.argv[1],".json")
#Ajouter un table
 
table=[[]]
dic={}
data_dict={}
dic[sys.argv[1]]=["bonjour"]
mon_tuple = (1, "ok", "olivier")
table.append("table1")
table[0].append(sys.argv[2])
table.append("table2")
print ("%s" %(table))
with open(argv, "w") as write_file:

    write_file.write(json.dumps(dic, indent=4))
    
   
