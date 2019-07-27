import redis
from parse import *
from counterOfRelation import*

#redis
redisLists = redis.StrictRedis(host='localhost',port=6379, db=0)

### set xmi-file
### if not readed from xml file: 
### new classes must be added (or removed) in classList: [['IDName','NameOfClass','Number']] (Number is unic and an integer that is added/ IDName is the ID in the xml-file, it can be same with Number)
### new relations must be added (or removed) in relation: [['AssociationName','IDName1','IDName2','Number of first class','Number of second class']]
### new package-list must be added (or removed) in packageList: [['IDNameOfPackage','NameOfPackage','IDNameofClass1','IDNameofClass2',....,'Number']]
### new package-relations must be added (or removed) in packageRelations: [['IDNameOfPackage1','IDNameOfPackage2']]
relation, classList, packageList, packageRelation=parseXMI('jgraphsrc a 1.2 xmi.xmi')
#print 'relation-list: ',relation,'\n'
#print 'package-relation',packageRelation
#print 'package-list',packageList,'\n'
#print 'class-list: ',classList,'\n'

### allRelFunc: get all Relations with the Caller and Callee Functions: [nameOfClass1,nameOfClass2, Caller-Function in Class1, Caller-Function in Class2]
### counterOfRel: get all Relations with number in a dictionary: *key of dict* => list of classes: [nameOfClass1,nameOfClass2] *value of dict* => counter of each relation: int
### some of the classes are dynamic. The functions coudn't be extracted!
allRelFunc, counterOfRel=counterOfRelation("JGraph- org REL.txt")
#print 'all relations with function calls: ',allRelFunc,'\n'
#print 'all counted relations: ',counterOfRel,'\n'

### Giving a list for all Relation functions: [['AssociationName','IDName1','IDName2','Number of first class','Number of second class','NameOfClass1','NameOfClass2', Counter]]
### Join Class and Relation
for rel in relation:
		for Class in classList:
			if rel[3]==Class[2]:
				rel.append(Class[1])
				break;
		for Class in classList:
			if rel[4]==Class[2]:
				rel.append(Class[1]) 
				break;

### Join Relation and Counter
for rel in relation:
	if str(rel[5:7]) in counterOfRel:
		rel.append(counterOfRel[str(rel[5:7])])

#Maybe we have some repeatet associations, we add them to the counter	

l=[]
repeat=[]
for i in relation:
	if i in l:
		repeat.append(i)
	else:
		l.append(i)

mainRelation=[]
for sublist in l:
	if sublist not in mainRelation and len(sublist)!=8:
		sublist.append(1)
		mainRelation.append(sublist)
	elif sublist not in mainRelation and len(sublist)==8:
		mainRelation.append(sublist)

for item in repeat:
	for rel in mainRelation:
		if item[0:7] == rel[0:7]:
			rel[7]=rel[7]+1
			break

redisLists.lpush('ClassList', classList)
redisLists.lpush('DefaultRelationList', mainRelation)
redisLists.lpush('OldRelationList', mainRelation)
redisLists.lpush('PackageList', packageList)
redisLists.lpush('PackageRelation', packageRelation)
redisLists.lpush('AllRelFunc', allRelFunc)

f=open("input.txt",'w')
for item in classList:
	f.write(str(item[0])+ " "+str(item[1])+" "+str(item[2])+"\n")

for item in mainRelation:
	f.write(str(item)+ "\n")

#for printing List:
#while(redisLists.llen('ClassList')!=0):
#	print(redisLists.lpop('ClassList'))


