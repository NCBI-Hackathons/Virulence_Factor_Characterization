import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.svm import LinearSVC
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import Binarizer

def train_model(path_to_csv):
	exp=pd.read_csv(path_to_csv,index_col=0)
	X = exp[exp.columns[13:]]
	y=exp['flag']
	yy=y
	#binarize the labels
	from sklearn.preprocessing import Binarizer
	#y = y.ravel().reshape(-1,1)
	#transformer = Binarizer(threshold=250).fit(y)
	#yy=transformer.transform(y)
	############Feature selection ############################3
	lsvc = LinearSVC(C=0.1, penalty="l1", dual=False).fit(X, yy.ravel())
	model = SelectFromModel(lsvc, prefit=True)
	X_new = model.transform(X)
	X_new.shape
	idxs_selected = model.get_support(indices=True)
	f = X.columns[idxs_selected]
	features_dataframe_new=X[f]

	#print(features_dataframe_new.shape)
	#print(list(features_dataframe_new))
	f = open("actual_pred",'w')
	#############################
	from sklearn.model_selection import LeaveOneOut
	loo = LeaveOneOut()
	loo.get_n_splits(features_dataframe_new)
	final_pred_discrete=[]
	final_pred=[];
	final_actual=[];
	for train_index, test_index in loo.split(features_dataframe_new):
		print("TRAIN:", train_index, "TEST:", test_index)
		X_train, X_test = features_dataframe_new.iloc[train_index], features_dataframe_new.iloc[test_index]
		y_train, y_test = yy[train_index], yy[test_index]
		#print(X_train, X_test, y_train, y_test)
		clf=SVC(kernel='linear',probability=True,class_weight="balanced")
		clf.fit(X_train, y_train.ravel())
		y_pred11 = clf.predict(X_test) 
		y_p_d=y_pred11.tolist()
		final_pred_discrete.extend(y_p_d)
		y_p_score=clf.predict_proba(X_test) ##### getting prob scores (coressponding to SVM score)
		y_t=y_test.tolist() # converting np array to list
		y_predicted=y_p_score.tolist()
		y_p_s1=[i[1] for i in y_predicted] # feteching 2nd element of 2 d array
		final_pred.extend(y_p_s1)
		final_actual.extend(y_t)
	#print(final_actual)
	#print(final_pred)
	#print(final_pred_discrete)
	res = "\n".join("{} {}".format(x, y) for x, y in zip(final_actual, final_pred))
	print(res,file=f)
	print(classification_report(final_actual, final_pred_discrete))
	print("AUROC")
	print(roc_auc_score(final_actual, final_pred))