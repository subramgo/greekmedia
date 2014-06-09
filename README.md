Multiclass classification problem.

vw --loss_function hinge data/wise2014-train.vw --binary

number of examples per pass = 12992000
passes used = 1
weighted example sum = 1.2992e+07
weighted label sum = -1.28064e+07
average loss = 0.00807774
best constant = -0.985716
total feature number = 3475306408


 vw --loss_function hinge  -d data/wise2014-train.vw -l 1 --binary --ngram 3 -f models/model-09-12-01.bin

finished run
number of examples per pass = 13165768
passes used = 1
weighted example sum = 1.31658e+07
weighted label sum = -1.29777e+07
average loss = 0.00688384
best constant = -0.985716
total feature number = 10452115968

real    11m42.021s
user    15m20.390s
sys     0m36.378s

 vw --loss_function hinge  -d data/wise2014-train.vw -l 1 --binary --ngram 3 -k -c --passes 10 -f models/model-09-12-01.bin

 finished run
number of examples per pass = 11849192
passes used = 4
weighted example sum = 4.73968e+07
weighted label sum = -4.67193e+07
average loss = 0.00685186 h
best constant = -0.985707
total feature number = 37627661409

real    40m29.367s
user    35m52.439s
sys     2m10.603s

 vw --loss_function hinge  -d data/wise2014-train-1.vw --binary  -f models/model-09-13-18.bin
 
number of examples per pass = 13165768
passes used = 1
weighted example sum = 1.31658e+07
weighted label sum = -1.29777e+07
average loss = 0.00458097
best constant = -0.985716
total feature number = 3519146694

real    9m49.423s
user    11m14.704s
sys     0m33.680s
