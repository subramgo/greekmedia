"""
	on line learning using scikit learning

"""

import sys
from sklearn.feature_extraction import FeatureHasher
from sklearn.preprocessing import label_binarize
from sklearn.linear_model.stochastic_gradient import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib

from collections import defaultdict
import numpy as np

###### Read input arguments ##############

input_file = sys.argv[1]
dev_file  = sys.argv[2]
model_file = sys.argv[3]
output_file = sys.argv[4]
train_or_test = sys.argv[5]

hasher = FeatureHasher()

BATCH_SIZE = 2000
y_classes = range(1,204)


def getXY(line):
	try:
		y, x = line.split( " ", 1 )
		x = x.rstrip()
		y = y.rstrip()

		y_entries =  y.split(",")
		y_entries = tuple(map(int,y_entries))

		x_entries =  x.split(" ")
		x_dict = defaultdict(float)
		for x_entry in x_entries:
			x = x_entry.split(':')
			feature_name = str(x[0])
			feature_value = float(x[1])
			x_dict['f'+feature_name] = feature_value

		return x_dict,y_entries
	except ValueError as e:
		print e
		return None,None



def loadDev(in_file):
	print 'Load dev set.'
	x_batch = []
	y_batch = []
	d = open ( in_file )

	for line in d:
		x_dict,y_entries = getXY(line)
		if x_dict != None and y_entries != None:
			x_batch.append(x_dict)
			y_batch.append(y_entries)

	x_new = hasher.fit_transform(x_batch)	
	y_new = label_binarize(y_batch,classes = y_classes, multilabel=True)

	return x_new,y_new


def test(input_file,model_file,output_file):
	print 'Start predicting'
	o = open( output_file, 'wb' )
	o.write( 'ArticleId,Labels\n'  )
	linecount = 64858
	records_processed = 0
	x_batch =[]
	y_batch =[]

	classifier_dict = joblib.load( model_file )
	i = open( input_file )
	for line in i:
		x_dict,y_entries = getXY(line)
		x_batch.append(x_dict)
		y_batch.append(y_entries)
		x_new = hasher.fit_transform(x_batch)	
		predicted_labels = ''
		confidence_scores =[]
		for i in range(1,204):
			p = classifier_dict[i].predict(x_new)
			q = classifier_dict[i].decision_function(x_new)
			confidence_scores.append(q[0])
			if p[0] == 1:
				predicted_labels+= str(i) + ' '
		if predicted_labels == '':
			p_sorted = sorted(range(len(confidence_scores)), key=confidence_scores.__getitem__)
			predicted_labels = str(p_sorted[len(p_sorted)-1]+1)


		predicted_labels = predicted_labels.strip()
		o.write(str(linecount) + "," + predicted_labels + "\n")
		linecount+=1
		records_processed+=1

		if records_processed%50 == 0:
			print 'Finished %d instances '%(records_processed)
		x_batch =[]
		y_batch =[]


def train(input_file,dev_file,model_file):
	x_batch =[]
	y_batch =[]
	classifier_dict = defaultdict(object)

	for i in range(1,204):
		classifier_dict[i] = SGDClassifier(loss='hinge')

	x_test,y_test = loadDev( dev_file )

	print 'Running in batchsize of %d'%(BATCH_SIZE)

	i = open( input_file )
	iteration =0

	for line in i:
		x_dict,y_entries = getXY(line)

		if x_dict != None and y_entries != None:
			x_batch.append(x_dict)
			y_batch.append(y_entries)

		if len(x_batch) == BATCH_SIZE:
			iteration+=1
			x_new = hasher.fit_transform(x_batch)	
			y_new = label_binarize(y_batch,classes = y_classes, multilabel=True)

			
			for i in range(1,204):
				clsf = classifier_dict[i]
				classifier_dict[i].partial_fit(x_new,y_new[:,i-1],classes=[0,1])
			
			
			total_accuracy=0
			
			for i in range(1,204):
				total_accuracy+=classifier_dict[i].score(x_test,y_test[:,i-1])
			avg_accuracy =total_accuracy/(1.0*203)
			
			print "After %d iteration(s), accuracy = %f " %(iteration,avg_accuracy)

			x_batch = []
			y_batch = []	

	############## Save the model #########################

	joblib.dump(classifier_dict, model_file)



if __name__ == "__main__":
	if train_or_test == "train":
		train(input_file,dev_file,model_file)
	else:
		test(input_file,model_file,output_file)
