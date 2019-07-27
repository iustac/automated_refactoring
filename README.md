# Automated refactoring
Automated refactoring is a refactoring tool that is implemented to refactor for projects Junit, Jgraph, JAG, FreeMind.
## Usage
First you should run ```pip install -r requirements.pip``` to install python dependencies. Next you should install [redis](https://redis.io/topics/quickstart) and [pyfuzzy](http://pyfuzzy.sourceforge.net/).\
After installing dependencies change directory to any project you want to test then run input file to initialize input values in redis. This file can be run by this command: ```python input.py```
In the last step run fuzzy_genetic file by ```python fuzzy_genetic.py```