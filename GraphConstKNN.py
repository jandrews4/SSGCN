import numpy as np
'''
this algorithm takes a sparse point cloud within 3d space and converts
it into a graph of many highly connected dense clusters and a set of far
less dense components. The algorithm works by taking an array of points
(x,y,z,n) where n is the vertex's number. Edges are of from (n1, n2, val)

This operates as a DBSCAN that has an *ADJUSTABLE* radius for graph construction 
IF the radius is too small THEN we do a KNN for that point
'''

#test cases
a = (0,0,0,'0')
b = (-1,-1,-1,'1')
c = (2, 4, 4, '2')
d = (.5, .5, .5, '3')

l = [a,b,c,d]

#calculates distance between points
def dist(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)


#iterates all points to get a unordered dictionary of tuples with 
# distances from p1 where l is the list of points

def alldist(p1, l):
    dic = {}
    for point in l:
        d = dist(p1, point)
        dic[point[3]] = d
    return dic

#sort the dictionary

def sorter(dict):
    return {key: val for key, val in sorted(dict.items(), key = lambda ele: ele[1])}

#make a list of vertex edge pairs of the form of a tuple 
#takes target vertex, sorted dict of nearest points. the direction is
#from vertex to vertex, arrow towards target point
def GenGraph(vert, dict, k):
    graph = []
    for i in dict:
        graph.append(i)
    return graph[1:k+1]

#now we put it all together to over all vertices and we have our graph, graph is structed of edges
#(start, end, dist) with arrows pointing from neighbor to target
def KNN(vertices, k):
    graph = []
    #vertices is a list of all points in the cloud of structure (x,y,z,n) n is the label
    for vertex in vertices:
        dict = alldist(vertex, vertices)
        sdict = sorter(dict)
        g = GenGraph(vertex, sdict, k)
        for i in g:
            graph.append((i, vertex[3],dict[i]))
    return graph



#future work: integrate radial graph const with knn from point cloud density
#KNN should apply to high density regions and radial for low density
#with radius changing based on particle density 
#big radius = low density, small rad = mid density, knn = high density
#ideally do radius based on density unless neighbors less than min,
#then do a KNN if this fails just do a separated process

        
#Determine density based on k neghbors avg distance 

sdi = sorter(alldist(a,l))

def density(k, sdict):
    avg = 0
    count = 0
    for a in sdict:
        avg += sdict[a]  
        if count == k+1:
            return avg/(count-1)
        count +=1
density(2, sdi)

def radgraph(point, sdict, density):
    graph = []
    for a in sdict:
        if density >= sdict[a]:
            graph.append((a, point))
    return graph

def GraphCon(k, points, eps):
    graph = []
    for p in points:
        print(p)
        sdict = sorter(alldist(p, points))
        d = density(k, sdict)
        if d <= eps:
            g = GenGraph(p, sdict, k)
            for i in g:
                graph.append(i)
        else:
            r = radgraph(p, sdict, d)
            for i in r:
                graph.append(i)
    return graph
print(GraphCon(2, l, 4))
