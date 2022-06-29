# Probe/Echo Algorithm Simulator

Python program that simulates the probe/echo algorithm used in distributed systems.
It can be used for information broadcasting and as an election algorithm. This particular
simulation uses it as an election algorithm, and the criteria for the leader is whoever has
the greated process id.

## Usage

First, write the topology of the system in the file named "adjacency_list.txt".
The syntax is the following: each line should have a list of integers separated by
space. The nodes pointed by node "i" are the numbers written in the i-th line.
For instance, the topology:

```
2
1 4
2 4
3 
```

Forms the following graph:

```
       3 <----.
       |      |
       V      V 
1 <--> 2 ---> 4 
```

With the topology decided, identify the number of nodes. In the above example, there
are 4 nodes in the system. Run that many number of CMDs and execute the python script
"candidate.py" on each one and input the corresponding node id. After that, open a new
CMD and run "simulator.py". It will ask for you to type the node that will start the
election, and after that, it will tell you the result. In the above example, the process
with the highest id is process 4, so it should return 4.
