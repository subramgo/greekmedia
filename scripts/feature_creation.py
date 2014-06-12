"""
Create vowpal wabbit training file from libsvn format
Prepare the data to convert k multi-label problem into K binary
classification problem
Use oaa format from vowpal wabbit

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
	line_count+=1
	try:
		y, x = line.split( " ", 1 )
		x=x.rstrip()
		no_words = len(x.split(" "))
		y_line = ''
		x_line = ''
		#  Handle multi-label
		given_ys = y.split(",")
		for ys in label_list:
			x_line+="LABEL_" + str(ys) + " " + x  + ' '#+ " NO_WORDS:" + str(no_words) + ' '
			if ys in given_ys:
				y_line+= str(ys) + ":0 "
			else:
				y_line+= str(ys) + ":1 "
		y_line+= " |"
		lines.append(y_line + x_line + "\n")

		if len(lines)%5000 == 0:
			for l in lines:
				o.write(l)
			print 'Done % lines'%(line_count)
			lines=[]

	except ValueError:
		print 'Value Error: ', line
if len(lines) > 0 :
	for l in lines:
		o.write(l)
