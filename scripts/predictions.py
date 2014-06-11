import socket
import sys
import math
import time

input_file 	= sys.argv[1]
output_file = sys.argv[2]

# List of labels
label_list =[str(ii) for ii in range(1,204)]
hostname = "127.0.0.1"
port = 26542

linecount = 64858
label_header = "LABEL"
buffer_size = 256

i = open( input_file )
o = open( output_file, 'wb' )

o.write( 'ArticleId,Labels\n'  )
lines_processed = 0

""" Netcat equivalent in python """
def netcat(contents,hostname="localhost", port=26542):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((hostname, port))
	predictions =[]
	for content in contents:
		s.sendall(content)

		while 1:
			data = s.recv(buffer_size)
			if data == "":
				break
			if data != "":
				predictions.append(data)
				break
	s.shutdown(socket.SHUT_WR)

	
	s.close()
	return predictions


def getVWFormat(line):
	y, x = line.split( " ", 1 )
	x=x.rstrip()
	no_words = len(x.split(" "))
	#x+=" NO_WORDS:" + str(no_words)
	vw_line = ''
	vw_list = ["|" + label_header + "_" + l + " " + x + ' ' for l in label_list]
	vw_entries = " ".join(vw_list)
	print vw_entries
	vw_list =[vw_entries + "\n"]
	return vw_list


def getPrediction(line):
	vw_instances = getVWFormat(line)
	prediction_list = []
	instance_count = 0
	prediction_list=netcat(vw_instances)
	print prediction_list
	prediction_list_float = map(float,prediction_list)
	prediction_labels = [i + 1 for i,x in enumerate(prediction_list_float) if x == 1.0]
	if len(prediction_labels) > 0:
		return prediction_labels
	else:
		p_sorted = sorted(range(len(prediction_list_float)), key=prediction_list_float.__getitem__)
		print p_sorted
		return [p_sorted[len(p_sorted)-1]+1]


for line in i:
	p = getPrediction(line.rstrip())
	lines_processed+=1
	if lines_processed%500 == 0:
		print "%d lines finished."%(lines_processed)
	p_str = " ".join(str(e) for e in p)
	o.write(str(linecount) + "," + p_str + "\n")
	linecount+=1








