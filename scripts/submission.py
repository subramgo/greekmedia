import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

i = open( input_file )
o  = open( output_file, 'wb' )
linecount = 64858
o.write( 'ArticleId,Labels\n'  )
for line in i:
	class_entry = int(float(line.rstrip()))
	o.write(str(linecount) + ',' + str(class_entry) + '\n')
	linecount+=1
