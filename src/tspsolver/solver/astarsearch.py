from sys import maxint
from ..core import Edge
from random import shuffle

def find(vertex, forest):
    for i in xrange(len(forest)):
        if vertex in forest[i]: return i

def closestCityDistance(edges, current, notVisited):
    for e in edges:
        if (e.source == current and e.target in notVisited) or (e.target == current and e.source in notVisited):
            return e.weight
 
def mst(edges, vertices):
    forest = [[v] for v in vertices]
    total = 0
    for edge in edges:
        if edge.target in vertices and edge.source in vertices:
            idxSource = find(edge.source, forest)
            idxTarget = find(edge.target, forest)
            if idxSource != idxTarget:
                forest[idxSource] = forest[idxSource] + forest[idxTarget]
                forest.pop(idxTarget)
                total += edge.weight
        if len(forest) == 1:
            return total

def literalDistance(edges, current, root):
    for e in edges:
        if (e.source == current and e.target == root) or (e.source == root and e.target == current):
            return e.weight

def f2(totalDistance, sparseMatrix, current, root, notVisited, nVertices):
    if current == root: return totalDistance
    return totalDistance + h2(sparseMatrix, current, root, notVisited, nVertices)

def f(totalDistance, edges, current, root, notVisited):
    if current == root: return totalDistance
    return totalDistance + h(edges, current, root, notVisited)

def h(edges, current, root, notVisited):
    if len(notVisited) == 0:
        return literalDistance(edges, current, root)
    return closestCityDistance(edges, current, notVisited) + mst(edges, notVisited) + closestCityDistance(edges, root, notVisited)

def closestDistanceToRoot(sparseMatrix, root, notVisited):
    minDistance = maxint
    for v in notVisited:
        if sparseMatrix[v.index][root.index] < minDistance:
            minDistance = sparseMatrix[v.index][root.index]
    return minDistance

def furthestDistanceToRoot(sparseMatrix, root, notVisited):
    maxDistance = 0
    for v in notVisited:
        if sparseMatrix[v.index][root.index] > maxDistance:
            maxDistance = sparseMatrix[v.index][root.index]
    return maxDistance

def h2(sparseMatrix, current, root, notVisited, nVertices):
    if len(notVisited) < nVertices/2:
        return closestDistanceToRoot(sparseMatrix,root, notVisited)
    return furthestDistanceToRoot(sparseMatrix,root, notVisited)

def edgeBetween(v1, v2, edges):
    e = Edge(v1,v2)
    return edges[edges.index(e)]
        
def astarSearch(graph):
    notVisited = list(graph.vertices)
    nVertices = len(notVisited)
    shuffle(notVisited)
    edges = list(graph.edges)
    current = notVisited[0] 
    root = notVisited[0]
    notVisited.remove(current)
    neighbors = dict(graph.neighbors)
    sparseMatrix = list(graph.sparseMatrix)
    distance = 0
    while current != root or len(notVisited) > 0:
        if len(notVisited) == 0:
            e = edgeBetween(current, root)
            distance += e.weight
            current = root
            continue
        minEstimate = maxint
        nextEdge = None
        for e in neighbors[current]:
            nextNode = None
            if root in e and root != current:
                continue
            if e.source == current:
                if e.target not in notVisited:
                    continue
                nextNode = e.target
            if e.target == current:
                if e.source not in notVisited:
                    continue
                nextNode = e.source
            aux = list(notVisited)
            aux.remove(nextNode)
            d = distance + e.weight
#            estimate = f(d,edges,nextNode,root,aux)
            estimate = f2(d,sparseMatrix,nextNode,root,aux, nVertices)

            if estimate < minEstimate:
                minEstimate = estimate
                nextEdge = e
        current = (nextEdge.target, nextEdge.source)[nextEdge.target == current]
        distance += nextEdge.weight
        notVisited.remove(current)

    return distance
