#Multi-label classification of print media article to topics.#

6/9/2014 2:13:52 PM 


[https://www.kaggle.com/c/wise-2014](https://www.kaggle.com/c/wise-2014)

[https://github.com/subramgo/greekmedia](https://github.com/subramgo/greekmedia)


There are 203 class labels, and each instance can have one or more labels. We convert this problem to a binary classification problem so that vowpal wabbit can handle it.

The data in libsvm format, we use scripts/feature_creation.py to convert them to vw format. For every instance, say

    103 1123:0.003061 1967:0.250931 3039:0.074709 20411:0.025801 24432:0.229228 38215:0.081586 41700:0.139233 46004:0.007150 54301:0.074447 .......
    
We create 203 vw entries as follows


    ....
    -1 |LABEL_102 1123:0.003061 1967:0.250931 3039:0.074709 20411:0.025801 24432:0.229228 38215:0.081586 41700:0.139233 46004:0.007150 54301:0.074447 .......NO_WORDS:17
    
    +1 |LABEL_103 1123:0.003061 1967:0.250931 3039:0.074709 20411:0.025801 24432:0.229228 38215:0.081586 41700:0.139233 46004:0.007150 54301:0.074447 .......NO_WORDS:17
     

As seen above we have added a new feature ***NO_WORDS***, to count the number of words.

Using vw we train it as follows

    vw --loss_function hinge  -d data/wise2014-train-1.vw --binary  -f models/model-09-13-18.bin
    
    number of examples per pass = 13165768
    passes used = 1
    weighted example sum = 1.31658e+07
    weighted label sum = -1.29777e+07
    average loss = 0.00458097
    best constant = -0.985716
    total feature number = 3519146694
    
For feature prediction, we run the model in daemon mode


    vw -i models/model-09-13-18.bin --daemon --quiet -t --port 26543

**scripts/prediction.py** is used to predict the test set.

This puts us in 16th place.

------

Feature Engineering
============

Using script **scripts/preprocess.py** we create a list of words which occur in more than 60% of the documents.
Running **scripts/dataReduction.py*** we