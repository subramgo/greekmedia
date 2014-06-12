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
import time,datetime

from optparse import OptionParser

hasher = FeatureHasher()

BATCH_SIZE = 100
NO_ITERATIONS = 2
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
		
		prediction_dict = defaultdict(list)
		decision_dict = defaultdict(list)


		if len(x_batch) == BATCH_SIZE:
			# Run a model per class on 'BATCH_SIZE' instances
			for i in range(1,204):
				p = classifier_dict[i].predict(x_new)
				q = classifier_dict[i].decision_function(x_new)
				assert len(p) == len(q)
				for recordNo,record in enumerate(p):
					if record == 1:
						prediction_dict[recordNo].append(i)
					decision_dict[recordNo].append(q[recordNo])

			# Print predictions
			for r in range(0,BATCH_SIZE):
				predicted_labels = []
				
				prediction_labels = prediction_dict[r]
				if len(prediction_labels) == 0:
					confidence_scores = decision_dict[r]
					p_sorted = sorted(range(len(confidence_scores)), key=confidence_scores.__getitem__)
					prediction_labels.append(p_sorted[len(p_sorted)-1]+1)	


				predicted_labels_string = " ".join(str(pl) for pl in prediction_labels)
				o.write(str(linecount) + "," + predicted_labels_string + "\n")
				linecount+=1
				records_processed+=1

				predicted_labels_string = ''
			
			print 'Finished %d instances - %s '%(records_processed,datetime.datetime.now())




			x_batch =[]
			y_batch =[]


	if len(x_batch) > 0:
		print "Finishing final %d instances"%(len(x_batch))
		# Run a model per class on 'BATCH_SIZE' instances
		for i in range(1,204):
			p = classifier_dict[i].predict(x_new)
			q = classifier_dict[i].decision_function(x_new)
			assert len(p) == len(q)
			for recordNo,record in enumerate(p):
				if record == 1:
					prediction_dict[recordNo].append(i)
				decision_dict[recordNo].append(q[recordNo])

		# Print predictions
		for r in range(0,len(x_batch)-1):
			predicted_labels = []
			
			prediction_labels = prediction_dict[r]
			if len(prediction_labels) == 0:
				confidence_scores = decision_dict[r]
				p_sorted = sorted(range(len(confidence_scores)), key=confidence_scores.__getitem__)
				prediction_labels.append(p_sorted[len(p_sorted)-1]+1)	


			predicted_labels_string = " ".join(str(pl) for pl in prediction_labels)
			o.write(str(linecount) + "," + predicted_labels_string + "\n")
			linecount+=1
			predicted_labels_string = ''
			



def train(input_file,dev_file,model_file):
	x_batch =[]
	y_batch =[]
	classifier_dict = defaultdict(object)

	for i in range(1,204):
		classifier_dict[i] = SGDClassifier(loss='hinge')

	x_test,y_test = loadDev( dev_file )

	print 'Running in batchsize of %d'%(BATCH_SIZE)

	in_file = open( input_file )


	for epoch in range(0,NO_ITERATIONS):
		iteration =0
		in_file.seek(0)
		print 'Running epoch = %d '%(epoch)
		for line in in_file:
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

		if len(x_batch) > 0:
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




	############## Save the model #########################

	joblib.dump(classifier_dict, model_file)



if __name__ == "__main__":

    usage = "usage: %prog [options] arg"
    
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="input_file",action="store",type="string",
                      help="training or testing data set file")
    parser.add_option("-d", "--dev",dest ="dev_file",action="store",type="string",
                      help="dev data set file")
    parser.add_option("-m", "--model",dest ="model_file",action="store",type="string",
                      help="dev data set file")
    parser.add_option("-o", "--output",dest ="output_file",action="store",type="string",
                      help="output file")
    parser.add_option("-t", "--train",dest ="train",action="store_true",default=True,
                      help="Is training or testing")
    parser.add_option("-p", "--predict",dest ="train",action="store_false",default=False,
                      help="Is testing")

    (options,arg) = parser.parse_args()

    is_train 	=  options.train
    input_file 	=  options.input_file
    dev_file 	=  options.dev_file
    model_file	=  options.model_file
    output_file =  options.output_file	


    if is_train :
		train(input_file,dev_file,model_file)
    else:
		test(input_file,model_file,output_file)
