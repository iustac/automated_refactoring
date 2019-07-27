import redis
from graph import *
from entropy import *
from outputCreator import *
from generate_shotgunSurgery import*
from generate_featureEnv import*
from generate_godClass import*
from generate_lazyClass import*
import ast

### generate the new popuation with respect to the badSmell: shotgunSurgery, featureEnv, godClass or lazy // classNumber: number of class // value: can be veryHigh, high, middle, low, veryLow 
### at the beginning: generate(start,'','',false)
### dataset changes with 'True'

def generate(BadSmellName,classNumber,value,boolean):
	
	#redis
	redisLists = redis.StrictRedis(host='localhost',port=6379, db=0)
	classList=ast.literal_eval(redisLists.lpop('ClassList'))
	defaultRelation=ast.literal_eval(redisLists.lpop('DefaultRelationList'))
	oldRelation=ast.literal_eval(redisLists.lpop('OldRelationList'))
	packageList=ast.literal_eval(redisLists.lpop('PackageList'))
	packageRelation=ast.literal_eval(redisLists.lpop('PackageRelation'))
	allRelFunc=ast.literal_eval(redisLists.lpop('AllRelFunc'))

	if boolean==True:
		relation=oldRelation
	else:
		relation=defaultRelation

	defaultRelation=relation[:]

	if BadSmellName=='feature_envy':
		updatedRelations=generate_featureEnv(classNumber,value, relation, classList, packageList, packageRelation)
	elif BadSmellName=='shotgun_surgery':
		updatedRelations=generate_shotgunSurgery(classNumber,value, relation, classList, packageList, packageRelation)
	elif BadSmellName=='god_class':
		updatedRelations=generate_godClass(classNumber,value, relation, classList, packageList, packageRelation)
	elif BadSmellName=='lazy_class':
		updatedRelations=generate_lazyClass(classNumber,value, relation, classList, packageList, packageRelation)
	if BadSmellName!='start':
		if updatedRelations!=[]:	
			for item in updatedRelations:
				for rel in relation:
					if item[0:7]==rel[0:7]:
						rel[7]=item[7]
						break
		relation=[s for s in relation if s[7] != 0]
				
	#Good examples:
	#newRelationList, updatedRelations=generate_featureEnv('3' , 'veryHigh', relation, classList, packageList, packageRelation, counterOfRel,allRelFunc)	
	#newRelationList, updatedRelations=generate_shotgunSurgery('1182' , 'veryLow', relation, classList, packageList, packageRelation, counterOfRel,allRelFunc)
	#newRelationList, updatedRelations=generate_godClass('3' , 'veryHigh', relation, classList, packageList, packageRelation, counterOfRel,allRelFunc)
	#newRelationList, updatedRelations=generate_lazyClass('3' , 'low', relation, classList, packageList, packageRelation, counterOfRel,allRelFunc)

	### get critical
	### cri: return critical classes in a list
	cri=get_critical(relation,classList)
	#print 'critical classes are: ',cri,'\n'

	### graph-properties
	### atr: return all class attributes in a list: Number, ID, Name, Degree C., InDegree C., OutDegree C. Betweenness C., Load C., Centrality C.-deleted
	### rel: returns all edge attributes in a list: RelationName, ID-edge1, ID-edge2, Nr.Edge1, Nr. Edge2, in this case it works like relation-deleted 
	G=get_graphAttributes(relation,classList)
	#print 'attribute of each class is: ',atr,'\n'

	### calculate entropy
	### ent: returns a list with values that represent how important a class is
	ent=get_entropy(relation,classList)
	#print 'entropy of each class is: ',ent,'\n'

	### get output-textfile for graph-attributes (+ edge-betweenness)
	get_output(classList,relation,cri,G,ent)

	redisLists.lpush('ClassList', classList)
	redisLists.lpush('DefaultRelationList', defaultRelation)
	redisLists.lpush('PackageList', packageList)
	redisLists.lpush('PackageRelation', packageRelation)
	redisLists.lpush('AllRelFunc', allRelFunc)
	redisLists.lpush('OldRelationList', relation)

# generate('start','','',False)
# generate('god_class','3','veryHigh',False)
# generate('shotgun_surgery','1182','veryLow',True)
