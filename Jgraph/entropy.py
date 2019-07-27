import numpy as np
from scipy.stats import entropy
from math import log
import copy

def entropy1(labels, base=None):
	value,counts = np.unique(labels, return_counts=True)
	return entropy(counts, base=base)

def get_entropy(relation,classList):
	ent=[]
	labels2=[]
	i=0
	for item in relation:
		labels2.append([])
		labels2[i].append(item[3])
		labels2[i].append(item[4])
		i=i+1
	each_label=[]
	each_label_self=[]
	for item in classList:
		i=0
		each_label=copy.deepcopy(labels2)
		each_label_self=[]
		for item2 in each_label:
			if item[2]==item2[0] or item[2]==item2[1]:
				each_label_self.append(each_label[i])
				each_label[i]=[]
			i=i+1
		j=0
		while each_label:
			if j>(len(each_label)-1):
				break
			if each_label[j]==[]:
				each_label.pop(j)
				j=0
			else:
				j=j+1
		ent.append([])
		ent[item[2]].append(item[2])
		try:
			ent[item[2]].append(float(entropy1(labels=each_label,base=None))/float(log(float(entropy1(labels=each_label,base=None))/float(entropy1(labels=each_label_self,base=None)),10)))
		except ZeroDivisionError:
			ent[item[2]].append(2**10000)
	return ent
