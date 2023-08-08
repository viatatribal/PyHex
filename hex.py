# This is a Hex game


# Graph to represent each player
graph = {
    'p1' : [],
    'p2' : []
}

# The board game is represented by a matrix nxn
board = [[0 for i in range(2)] for i in range(2)]

# dfs function
visited = set()
def dfs(visited, graph, node):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

# set position in board
def setPosition(x,y, player):
    board[x][y] = x + y
    graph[player].append(x+y)
    if x+y not in graph:
        graph[x+y] = []


