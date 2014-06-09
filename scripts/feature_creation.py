"""
Create vowpal wabbit training file from libsvn format
Prepare the data to convert k multi-label problem into K binary
classification problem

Added a feature for word_count
"""
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

i = open( input_file )
o = open( output_file, 'wb' )

# List of labels
label_list =[str(ii) for ii in range(1,204)]
label_header ="LABEL"
lines =[]
line_count = 0
for line in i:
	print "Processing Line = %d"%(line_count)
	line_count+=1
	try:
		y, x = line.split( " ", 1 )
		x=x.rstrip()
		no_words = len(x.split(" "))
		x+=" NO_WORDS:" + str(no_words)
		#  Handle multi-label
		given_ys = y.split(",")
		for ys in label_list:
			if ys in given_ys:
				new_line =  "1 |" + label_header + "_" + ys + " " + x + "\n"
				lines.append(new_line)
			else:
				new_line =  "-1 |" + label_header + "_" + ys + " " + x + "\n"
				lines.append(new_line)

		if len(lines)%1000 == 0:
			for l in lines:
				o.write(l)
			print 'Writen 10000 lines'
			lines=[]

	except ValueError:
		print 'Value Error: ', line
if len(lines) > 0 :
	for l in lines:
		o.write(l)
