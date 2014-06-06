import socket
import sys
import math

input_file 	= sys.argv[1]
output_file = sys.argv[2]

# List of labels
label_list =[str(ii) for ii in range(1,204)]
hostname = "localhost"
port = 26542

linecount = 64858
label_header ="LABEL"


i = open( input_file )
o = open( output_file, 'wb' )

o.write( 'ArticleId,Labels\n'  )

def netcat(content,hostname="localhost", port=26542):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        if data != "":
        	prediction = data

    s.close()
    return prediction


def getVWFormat(line):
	y, x = line.split( " ", 1 )
	vw_list = ["|" + label_header + "_" + l + " " + x + '\n' for l in label_list]
	return vw_list


def getPrediction(line):
	vw_instances = getVWFormat(line)
	prediction_list=list(map(netcat,vw_instances))
	prediction_list_float = map(float,prediction_list)
	print prediction_list_float
	print 
	return [i + 1 for i,x in enumerate(prediction_list_float) if x == 1.0]


for line in i:
	p = getPrediction(line.rstrip())
	print p
	print 
	p_str = ",".join(str(e) for e in p)
	o.write(str(linecount) + "," + p_str + "\n")
	linecount+=1








