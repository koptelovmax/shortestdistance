import networkx as nx
import numpy as np
import timeit

def orion_distance(CoordArr,A,B,d):
    
    distance = 0
    for i in range(d):
        distance += (CoordArr[A,i] - CoordArr[B,i])**2
        
    return round(np.sqrt(distance))

start = timeit.default_timer() # Initialize the timer to compute the time

# Input parameters:
network_name = 'last-fm-giant'
dimensions = 10
num_test = 100

# Load the Graph:
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

# Load the Graph Coordinate System:
GCS = np.zeros((n,dimensions))
f = open('Orion-files\\MyResults-'+network_name+'.txt', 'r')
for line in f:
    try:
        data = line.split(' ')
        X = [float(i) for i in data[2:2+dimensions]]
        GCS[np.int(data[1]),:] = X
    except ValueError:
        print "Invalid input:", line
f.close()

# Load the test nodes and perform tests:
count = 0
max_error = 0
sum_error = 0

G = nx.Graph()
f = open('tests\\'+network_name+'-tests.txt', 'r')
for line in f:
    try:
        data = line.split(' ')
        dist_estimated = orion_distance(GCS,np.int(data[0]),np.int(data[1]),dimensions)
        relative_error = np.abs(dist_estimated-np.int(data[2]))/np.int(data[2])
        sum_error += relative_error
        if relative_error > max_error:
            max_error = relative_error
        count += 1
        
    except ValueError:
        print "Invalid input:", line
f.close()

RAE = sum_error/count

print 'Number of tests: ',count
print 'Average Relative Error: ',RAE
print 'Maximum Relative Error: ',max_error
        
stop = timeit.default_timer() # stop the time counting
print 'Time spent, sec: ',stop-start
