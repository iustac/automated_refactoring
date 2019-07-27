from xml.dom import minidom
def parseXMI(my_file):
	classList=[]
	packageList=[]
	i=0
	j=0
	xmldoc = minidom.parse(my_file)

	### for package and their classes 	
	for package in xmldoc.getElementsByTagName("UML:Package"):
		packageList.append([])
		packageList[j].append(str(package.getAttribute('xmi.id')))
		packageList[j].append(str(package.getAttribute('name')))
		for element in package.getElementsByTagName("UML:Class"):
			packageList[j].append(str(element.getAttribute('xmi.id')))
		packageList[j].append(j)
		j=j+1

	### for classes
	for element in xmldoc.getElementsByTagName("UML:Class"):
		classList.append([])
		classList[i].append(str(element.getAttribute('xmi.id')))
		classList[i].append(str(element.getAttribute('name')))
		classList[i].append(i)
		i=i+1
	
	#for element in xmldoc.getElementsByTagName("UML:Interface"):
	#	classList.append([])
	#	classList[i].append(str(element.getAttribute('xmi.id')))
	#	classList[i].append(str(element.getAttribute('name')))
	#	classList[i].append(i)
	#	i=i+1

	### make relation-list for the classes. 
	### find the relations and insert them in the matrix
	relation=[];
	relation.append([])
	i=0;

	### generalization
	for element in xmldoc.getElementsByTagName("UML:Generalization"):
		relation.append([])
		relation[i].append('generalization')
		relation[i].append(str(element.getAttribute('parent')))
		relation[i].append(str(element.getAttribute('child')))
		i=i+1

	### aggregations-association,composition,aggregation
	twice=False	
	for e in xmldoc.getElementsByTagName("UML:Association.connection"):
		for element in e.getElementsByTagName("UML:AssociationEnd"):
			if twice==False:
				if str(element.getAttribute('aggregation'))=='none':
					relation[i].append('association')
				else:
					relation[i].append(str(element.getAttribute('aggregation')))
			relation[i].append(str(element.getAttribute('participant')))
			twice=True
		i=i+1
		relation.append([])	
		twice=False
	relation=relation[:-1]

	for i in relation:
		for item in classList:
			if i[1]==item[0]:
				i.append(item[2])
			if i[2]==item[0]:
				i.append(item[2])

	### for removing relations with interfaces
	relation = filter(None, relation)
	rLen=len(relation)
	sub=0
	for i in range(rLen):
		i=i-sub
		try:
			gotdata = relation[i]
		except IndexError:
			break
		if len(relation[i])!=5:
			relation.remove(relation[i])
			sub=sub+1


	for i in relation:
		if(i[0]=='composite' or i[0]=='aggregate' or i[0]=='generalization'):
			b=i[1]
			i[1]=i[2]
			i[2]=b
			b=i[3]
			i[3]=i[4]
			i[4]=b

	
	### make relation-list for the packages. 
	packageRelation=[];
	packageRelation.append([])
	pCounter=0
	first=True
	for item in relation:
		for package in packageList:
			if (item[1] in package and first) or (item[2] in package and first):
				packageRelation[pCounter].append(package[0])
				first=False
			elif (item[1] in package and first==False) or (item[2] in package and first==False):
				packageRelation[pCounter].append(package[0])
				first=True
				pCounter=pCounter+1
				packageRelation.append([])
				break
		if first==False:
			first=True
			pCounter=pCounter+1
			packageRelation.append([])

	

	### Keep just the relations in the packageRelation-list
	packageRelation = filter(None, packageRelation)
	pLen=len(packageRelation)
	sub=0
	for i in range(pLen):
		i=i-sub
		try:
			gotdata = packageRelation[i]
		except IndexError:
			break
		if len(packageRelation[i])!=2:
			packageRelation.remove(packageRelation[i])
			sub=sub+1
		

	return relation,classList,packageList,packageRelation
