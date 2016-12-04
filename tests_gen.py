import networkx as nx
import numpy as np
import timeit

start = timeit.default_timer() # Initialize the timer to compute the time

# Input parameters:
network_name = 'RoadNet-PA'
num_test = 100

# Load the data:
G = nx.Graph()
f = open('datasets\\'+network_name+'.txt', 'r')
for line in f:
    try:
        data = line.split(' ')
        #X = [int(i) for i in data[:2]]
        #G.add_nodes_from([np.int(data[0]),np.int(data[1])])
        G.add_edge(np.int(data[0]),np.int(data[1]))
    except ValueError:
        print "Invalid input:", line
f.close()
n = G.number_of_nodes()

# Generate the tests:
test_nodes = np.random.random_integers(0,n-1,num_test)
nodes = G.nodes()
count = 0

with open('tests\\'+network_name+'-tests.txt', "w") as test_file:
    for i in range(num_test):
        for j in range(i+1,num_test):
            if nx.has_path(G,nodes[test_nodes[i]],nodes[test_nodes[j]]) and (test_nodes[i] != test_nodes[j]):
                test_file.write(np.str(nodes[test_nodes[i]])+' '+np.str(nodes[test_nodes[j]])+' '+np.str(nx.shortest_path_length(G,nodes[test_nodes[i]],nodes[test_nodes[j]]))+"\n")
                count += 1
        print i+1

print count
        
stop = timeit.default_timer() # stop the time counting
print 'Time spent, sec: ',stop-start
