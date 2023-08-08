# This is a Hex game


# Graph to represent each player
graph = {
    'p1': [],
    'p2': []
}

# a dictionary that check if a piece belongs to player 1 or player 2
pieces = {
    'p1': [],
    'p2': []
}

# size of board
N = 2
# The board game is represented by a matrix nxn
board = [[0 for i in range(N)] for i in range(N)]

# all positions in the left side of the board ignoring the first and last one
leftboard = [i*N+1 for i in range(1,N-1)]
# all positions in the right side of the board ignoring the first and last one
rightboard = [i*N for i in range(2,N)]

# positions to check if any of the players won the game
p1winpos = [i*N for i in range(1,N+1)]
p2winpos = [(N-1)*N+i for i in range(1,N+1)]


def winGame(node, player):
    """Check if any of the players won the game."""
    if player == 'p1' and node in p1winpos:
        return True
    elif node in p2winpos:
        return True
    else:
        return False


def dfs(node, player):
    """Depth-first search algorithm to check if any of the players connected their sides."""
    visited = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if n not in visited:
            visited.add(n)
        elif n in visited:
            continue
        if winGame(n, player):
            return True
        for neighbour in graph[n]:
                stack.append(neighbour)
    return False


def addNodes(pos, node):
    """Connect two nodes in a graph."""
    graph[pos].append(node)
    graph[node].append(pos)


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


def checkNeighbour(pos, neighbours, player):
    """We check if any of the pos's neighbours is in the graph, if so we
       connect their edges as long as they are from the same player."""
    for n in neighbours:
        if n in graph and n in pieces[player]:
            addNodes(pos, n)


def setPosition(x,y,player):
    """Set the pieces for each player, then update the pieces owner per player
       and update nodes connections."""
    pos = x*N + y + 1
    board[x][y] = pos
    pieces[player].append(pos)
    # here we check if player 1 placed any piece in the left column
    if (pos-1) % N == 0 and player == 'p1':
        graph['p1'].append(pos)
    # or if the player 2 placed any piece in the first row
    if x == 0 and player == 'p2':
        graph['p2'].append(pos)
    if pos not in graph:
        graph[pos] = []
    checkNeighbour(pos, genNeighbour(pos), player)


# this function exists only until I use pygame
def game():
    players = ['p1', 'p2']
    i = 0
    running = True
    while running:
        x = int(input("Enter x position: "))
        y = int(input("Enter y position: "))
        setPosition(x,y,players[i])
        for n in graph[players[i]]:
            if dfs(n, players[i]):
                print(players[i] + " win!")
                print(pieces)
                print(graph)
                print(board)
                running = False
                break
        i = (i+1) % 2

game()
