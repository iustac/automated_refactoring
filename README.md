# Automated refactoring
Automated refactoring is a refactoring tool that is implemented to find bad smells in java projects like Junit, Jgraph, JAG and FreeMind and also to refactor them. You can also refactor any other java code by replacing the input file.
## Usage
### Installation
First, you should run ```pip install -r requirements.pip``` to install python dependencies. 
Next, you should install [redis](https://redis.io/topics/quickstart) and [pyfuzzy](http://pyfuzzy.sourceforge.net/).
### Running the code
After installing the dependencies change directory to any project you want to test, then run the input file to initialize input values in redis. This file can be run by this command: ```python input.py```
In the last step run fuzzy_genetic file by ```python fuzzy_genetic.py```
### Running a new java code
If you want to refactor your Own code you need the xmi-file and the call-relation of your java code. You just have to change the paths in the input.py file.
You can get the xmi-file of your code with tools like Visual Paradigm. To get the call-relation of your code you can use the [java-callgraph](https://github.com/gousiosg/java-callgraph) library .
### The results
In the end, you can see the results in the result.txt and not_refactor.txt. The class-ids of each class that had a bad smell and have been refactored is in the result-file. In the not_refactor-file are class-ids of classes that have a bad smell but couldn't been refactored. In the end, you can also see the output.txt file which gives you a new refactored structure of the class-graph and their right relations in a graph. If you are interested you can convert this structure again to the UML-Diagramm to see the changes in the relations.
