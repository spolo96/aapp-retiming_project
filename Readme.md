# Summer Session Project on Advanced Algorithms

# Retiming of a Graph

Problem: Optimize the frequency of a circuit
Solutions: Move register(s) so that 
	clock cycle decreases, or number of registers decreases and
	input-output behavior is preserved

## Description

The following project is an implementation and profiling of the paper [1] with separate algorithms that the user can manipulate.

## Getting Started

### Dependencies

* User must have python3-graph-tool installed.
* matplotlib
* numpy
* time
* sys

### Installation

* Official and more general instructions can be found [here](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).
* For the project, a Window Subsystem for Linux (WSL) was used, the instructions are:
    * add the following line to your /etc/apt/sources.list:
    ```
    deb [ arch=amd64 ] https://downloads.skewed.de/apt DISTRIBUTION main
    ```
    where DISTRIBUTION can be any one of
    ```
    bullseye, buster, sid, bionic, eoan, focal
    ```
    You should then download the public key 612DEFB798507F25 to verify the packages, with the command:
    ```
    apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
    ```
    After running apt-get update, the package can be installed with
    ```
    apt-get install python3-graph-tool
    ```

## Program Execution

The project consists of various implemented algorithms: CP, WD, OPT1, OPT2, graphGenerator, graphCorrelator that the user can manipulate with random generated graphs or user-input graphs.

### Python Environment

#### RetimingProject_Main

This is the general algorithm that contains the previous mentioned algorithms that is ready for the user usage. In order to begin to use the tool we need to open python3-graph-tool and write the following command:
```
from RetimingProject_Main import *
```
This will load all the needed algorithms into the python environment along with an already created graph example that is correlator 1 from [1].

Since the graph is already created and saved into the g variable, we can perform methods like this:
```
OPT1(g)
``` 
which will execute and give us specific results depending on the algorithm we used.

#### graphGenerator - graphCorrelator

We can also easily create a graph correlator similar to the examples from [1] or a general graph that respects the constraints of the graph generation with a single command line like this:
```
g = graphGenerator(n) #n is an arbitrary size of nodes

correlator = graphCorrelator(n) #Or we can create a correlator. 
```
Then we can use any of the algorithms with the previous created graph:
```
OPT2(correlator)
```

### Profiling

Two scripts were made in order to automatically check the performance and the memory usage of the implemented algorithms. Each script calculates the time/memory used by each OPT1 and OPT2 algorithms by varying the number of nodes and edges by a fixed increasing size. 

After each script is run, a graph image will be generated showing the performance of both algorithms depending of the profiling.

An additional script was made in order to check at the same time the performance and the memory usage of both algorithms.

* timeProfiler.py: calculates the time taken from each algorithm with a specific max range for the nodes of the graph.

* memoryProfiler.py: calculates the memory usage from each algorithm with a specific max range for the nodes of the graph.

* profiler.py: calculates both the time and the memory used by both algorithms. 

#### Instructions

Each profiler function must be called in a standard command line shell like the following example: 
```
python3 profiler.py [graphType] [maxNodeInput]
```
where the command line takes two inputs: 
* graphType: the type of graph to profile, it can be either ```generator``` or ```correlator```
* maxNodeInput: the maximum number of nodes that the final graph will have multiplied by 10. This needs to be a number greater than 1. 

So for example, we may want to profile how much time and memory a graph correlator uses from 10 nodes to 100 nodes. We would write the command like this:

```
python3 profiler.py correlator 10
``` 

The reason we write 10 as the maxNodeInput and not 100 is because the profiler adds 10 nodes within each iteration, meaning that the profiler will calculate the performance in the first iteration with 10 nodes, the second with 20 nodes, the third with 30 until the last one multiplied by 10, which in our case the final iteration will be with 100 nodes. 

The same applies to both ```memoryProfiler.py``` and ```timeProfiler.py``` which can be also called from the command line to make the respective profilings as:

```
python3 timeProfiler.py generator 10
```
or
```
python3 memoryProfiler.py correlator 5 
```
For example, the previous profiling will stop until 50 nodes are created and executed with OPT1 and OPT2.

### Colab Version
There is also ready-to-use python notebook in Colab in case the local installation went wrong or if the user wants to test the algorithm as soon as possible. This version has the general algorithm with all the methods that the user can manipulate with its own graphs or the random retiming ones. 

#### Usage

Since the environment is run in IPython, the user can write the same commands as before:
```
g = graphCorrelator(n)

OPT1(g)
```
which will execute according to the algorithm used.

## References

* [1] [Leiserson, C. E., & Saxe, J. B. (1991). Retiming synchronous circuitry. Algorithmica, 6(1-6), 5-35.](https://link.springer.com/article/10.1007/BF01759032)
* [Official Graph-Tool Documentation](https://graph-tool.skewed.de/static/doc/index.html)
* [Profiling and Timing Code](https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html)
* [snakeviz](https://jiffyclub.github.io/snakeviz/)