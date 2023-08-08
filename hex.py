# This is a Hex game


# Graph to represent each player
graph = {
    'p1' : [],
    'p2' : []
}

# size of board
N = 2
# The board game is represented by a matrix nxn
board = [[0 for i in range(N)] for i in range(N)]

# dfs function
visited = set()
def dfs(visited, graph, node):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

#  add nodes to the graph
def addNodes():
    pass


# generate all neighbour of a given position
def genNeighbour(pos):
    pass


# check the neighbour of a position
# so we can add it to the graph
def checkNeighbour(x,y, neighbour):
    for n in neighbour:
        pass


# set position in board
def setPosition(x,y, player):
    pos = x*N + y + 1
    board[x][y] = pos
    graph[player].append(pos)
    if pos not in graph:
        graph[pos] = []

