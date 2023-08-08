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

# all positions in the left side of the board ignoring the first and last one
leftboard = [i*N+1 for i in range(1,N-1)]
# all positions in the right side of the board ignoring the first and last one
rightboard = [i*N for i in range(2,N)]

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


def genNeighbour(pos):
    """Given a position, we return all its neighbour in a vector. We need to check what position
       in the board we are so we don't generate invalid neighbours."""
    if pos == 1:                                    # first position of first row
        return [pos+1,N+1]
    elif 1 < pos < N:                               # first row
        return [pos-1, pos+1, pos+N-1, pos+N]
    elif pos == N:                                  # last position of first row
        return [pos-1, pos+N-1, pos+N]
    elif pos == (N-1)*N+1:                          # first position in the last row
        return [pos-N, pos-N+1, pos+1]
    elif pos == N*N:                                # last position of the last rown
        return [pos-N, pos-1]
    elif pos in leftboard:                          # any position in the left side of the board
        return [pos-N, pos-N+1, pos+1, pos+N]
    elif pos in rightboard:                         # any position in the right side of the board
        return [pos-N, pos-1, pos+N-1, pos+N]
    elif (N-1)*N+1 < pos < N*N:                     # any position in the last rown
        return [pos-N, pos-N+1, pos-1, pos+1]
    else:                                           # all other positions
        return [pos-N, pos-N+1, pos-1, pos+1, pos+N-1, pos+N]

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

