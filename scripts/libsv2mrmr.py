"""
	Convert libsvm format to mRMR format
	http://penglab.janelia.org/proj/mRMR/#data
"""
import sys
from collections import defaultdict
import numpy as np
import operator

INPUT_FILE  = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

i = open( INPUT_FILE )
o = open( OUTPUT_FILE, 'wb' )

feature_dict = defaultdict(int)

feature_index =0

for line in i:
	try:
		y, x = line.split( " ", 1 )
		x=x.rstrip()
		ind_features = x.split(" ")
		for f in ind_features:
			f_name = int(f.split(":")[0])
			if feature_dict[f_name] == 0:
				feature_index+=1
				feature_dict[f_name]=feature_index
	except ValueError as e:
		print e

print 'No of features = %d '%(feature_index)
sorted_feature_dict = sorted(feature_dict.iteritems(), key=operator.itemgetter(1))

header_string = 'class'

for item in sorted_feature_dict:
	header_string+=',' + str(item[0])

o.write(header_string + "\n")

row_array = np.zeros(feature_index)

i.seek(0)
for line in i:
	try:
		y, x = line.split( " ", 1 )
		x=x.rstrip()
		ind_features = x.split(" ")
		for f in ind_features:
			f_name_value = f.split(":")
			f_name = int(f_name_value[0])
			f_value = float(f_name_value[1])
			f_index = feature_dict[f_name]
			if f_index != 0:
				row_array[f_index-1] = f_value
		row_array_char = np.char.mod('%f',row_array)
		row_string = str(y) + "," + ",".join(row_array_char)
		o.write(row_string + "\n")

	except ValueError as e:
		print e
