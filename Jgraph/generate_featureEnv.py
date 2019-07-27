from random import randint
from operator import itemgetter
import ast

def generate_featureEnv(classNumber, value, relation, classList, packageList, packageRelation):
	onlyRelation=[]	#only relations for a special class
	numberOfRel=0
	numberOfClassInRel=0
	numChange=0
	average=0
	package=[]

#Find all Relations for this class and count them	
#Only association
	for rel in relation:
		if str(rel[3])==str(classNumber) and rel[0]=='association':
				onlyRelation.append(rel)

	for item in packageList:
		if onlyRelation == []:
			break
		if onlyRelation[0][1] in item:
			package=item
			break

#for featureEnv we want to remove the most related Relations.  
	for item in onlyRelation:
		if item[7]>1:
			numberOfClassInRel=numberOfClassInRel+1
			numberOfRel=numberOfRel+item[7]
	if numberOfClassInRel!=0:
			average=round(numberOfRel/numberOfClassInRel)

# 1 is always the "veryLow' 
	if value=="very_high":
		numChange=2*average #Joda chetori??
	elif value=="high":
		numChange=round(average*3/2)
	elif value=='middle':
		numChange=average
	elif value=='low':
		numChange=round((average+1)/2)
	elif value=='very_low':
		numChange=1

#FeatureEnv
#Delete Relations-> Priority: 1. Most Relations 2. Not the only relation for Packages
	package2=""
	i=0
	flag=False #for not finding one because of package or when zero
	answer=[]
	while i < int(round(numChange)): #not more then change
		ID2=""
		if len(onlyRelation)==0: #can be zero because of the package relation
			break
		if flag==False:
			onlyRelation=sorted(onlyRelation, key=itemgetter(7), reverse=True) #always the biggest
		else:
			answer.append(onlyRelation[0])
			onlyRelation=sorted(onlyRelation[1:], key=itemgetter(7), reverse=True) #when biggest can't be remove because of the package relation, we sort it from the second one
			if len(onlyRelation)==0: #if zero 
				break
			flag=False
		if onlyRelation[0][7]==1 and package!=[]:
			for j in classList:
				if str(onlyRelation[0][4])==str(j[2]):
					ID2=j[0]
					break
			if ID2 not in package:
				for pac in packageList:
					if ID2 in pac:
						package2=pac
						break
				if package2!=[] and package!=[]:
					for pacRel in packageRelation:
						if package2[0] in pacRel and package[0] in pacRel and len(intersection(package, package2))>1:
							onlyRelation[0][7]=	onlyRelation[0][7]-1
							i=i+1
							if onlyRelation[0][7]==0:
								flag=True
							break
						else:
							flag=True
				else:
					onlyRelation[0][7]=	onlyRelation[0][7]-1
					i=i+1
					if onlyRelation[0][7]==0:
						flag=True
			else:
				onlyRelation[0][7]=	onlyRelation[0][7]-1
				i=i+1
				if onlyRelation[0][7]==0:
					flag=True
		else:
			onlyRelation[0][7]=	onlyRelation[0][7]-1
			i=i+1
			if onlyRelation[0][7]==0:
				flag=True
		
	answer.append(onlyRelation)
	return answer


