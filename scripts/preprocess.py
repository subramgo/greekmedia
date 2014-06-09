import sys
from collections import defaultdict

input_file = sys.argv[1]
output_file = sys.argv[2]

i = open( input_file )
o  = open( output_file, 'wb' )

word_count = defaultdict(int)
line_count = 0
for line in i:
	line_count+=1
	try:
		y, x = line.split( " ", 1 )
		x=x.rstrip()
		words = x.split(" ")
		for w in words:
			word = w.split(":")
			word_count[word[0]]+=1
	except ValueError as e:
		print e,y

for k,v in word_count.items():
	if v/(1.0*line_count) < 0.6:
		o.write(str(k) + " : " + str(v) + "\n")



