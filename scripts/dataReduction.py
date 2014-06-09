import sys
from collections import defaultdict

input_file = sys.argv[1]
dict_file = sys.argv[2]
output_file = sys.argv[3]


d = open( dict_file )
key_words_dict = defaultdict(int)

for l in d:
	key_value = l.split(":")
	key_words_dict[int(key_value[0])] = 1


i = open( input_file )
o = open( output_file, 'wb' )


for line in i:
	try:
		y, x = line.split( " ", 1 )
		x=x.rstrip()
		words = x.split(" ")
		new_x = ''
		for w in words:
			word = w.split(":")
			if key_words_dict[int(word[0])] != 0:
				new_x+= str(word[0]) + ':' + str(word[1]) + ' '
		o.write(str(y) + ' ' + new_x.strip() + '\n')
	except ValueError as e:
		print e

