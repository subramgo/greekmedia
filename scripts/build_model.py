from sklearn.datasets import load_svmlight_file

X_train, y_train = load_svmlight_file("../data/wise2014-train.libsvm", dtype=np.float64, multilabel=True)

X_test, y_test = load_svmlight_file("../data/wise2014-test.libsvm", dtype=np.float64, multilabel=True)


