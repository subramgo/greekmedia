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
label_header = "LABEL"
buffer_size = 256

i = open( input_file )
o = open( output_file, 'wb' )

o.write( 'ArticleId,Labels\n'  )
lines_processed = 0

def netcat(content,hostname="localhost", port=26542):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(buffer_size)
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
	prediction_labels = [i + 1 for i,x in enumerate(prediction_list_float) if x == 1.0]
	if len(prediction_labels) > 0:
		return prediction_labels
	else:
		p_sorted = sorted(range(len(prediction_list_float)), key=prediction_list_float.__getitem__)
		return [p_sorted[len(p_sorted)-1]+1]


for line in i:
	p = getPrediction(line.rstrip())
	lines_processed+=1
	if lines_processed%25 == 0:
		print "%d lines finished."%(lines_processed)
	p_str = ",".join(str(e) for e in p)
	o.write(str(linecount) + "," + p_str + "\n")
	linecount+=1








