import networkx as nx
import numpy as np
import collections
import timeit

start = timeit.default_timer() # Initialize the timer to compute the time

# Input parameters:
network_name = 'co-dblp'
num_landmarks = 30

# Load the dataset:
G = nx.Graph()
f = open('datasets\\'+network_name+'.txt', 'r')
for line in f:
    try:
        data = line.split(' ')
        #X = [int(i) for i in data[:2]]
        #G.add_nodes_from([np.int(data[0]),np.int(data[1])])
        G.add_edge(np.int(data[0]),np.int(data[1]))
    except ValueError:
        print 'Invalid input:', line
f.close()
n = G.number_of_nodes()

# Obtain landmarks:
## 1st way: randomly - uncomment if you want to use this way:
##l = np.random.randint(0,G.number_of_nodes()-1,(1,num_landmarks)) 

# 2-nd way: using degree centrality
l = np.zeros((1,num_landmarks),np.int)

count = 0
for i,j in collections.Counter(nx.degree_centrality(G)).most_common(num_landmarks):    
    l[0,count] = i
    count += 1    

# Obtaining GCS input file:
with open('landmarks\\'+network_name+'-landmarks.txt', 'w') as landmark_file:
    with open('Orion-files\\input_GCS-'+network_name+'.txt', 'w') as GCS_input_file:
        for i in range(num_landmarks):
            for j,k in nx.single_source_shortest_path_length(G,l[0,i]).items():
                GCS_input_file.write(np.str(l[0,i])+' '+np.str(j)+' '+np.str(k)+'\n')
            landmark_file.write(np.str(l[0,i])+' ')

stop = timeit.default_timer() # stop the time counting
print 'Time spent, sec: ',stop-start

# Some statistics to check:
print 'Number of nodes: ',G.number_of_nodes()
print 'Number of edges: ',G.number_of_edges()
print 'Is the graph connected? ',nx.is_connected(G)
print 'Number of self-loops: ',G.number_of_selfloops()