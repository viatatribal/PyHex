# This is a Hex game

import pygame


# for clickables rectangles
class Pieces:
    def __init__(self, x, y, w, h, pos):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pos = pos
        self.clickable = True
        self.image = {'p1' : pygame.image.load("p1.png").convert_alpha(),
                      'p2' : pygame.image.load("p2.png").convert_alpha()}

    def setImage(self, player):
        self.player = player

    def getImage(self):
        return self.image[self.player]


# for the main game loops
class Game:
    def __init__(self, window, board):
        self.window = window
        self.board = board
        self.running = True
        self.end = False
        self.player = 'p1'
        self.winner = None

    def ending(self):
        self.end = True
        self.winner = pygame.image.load(self.player + "win.png").convert()

    def quit(self):
        self.running = False

    def changePlayer(self):
        self.player = 'p2' if self.player == 'p1' else 'p1'


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
# size of the window
screenSize = (800,485)
# size of board
N = 11
# all positions in the left side of the board ignoring the first and last one
leftboard = [i*N+1 for i in range(1,N-1)]
# all positions in the right side of the board ignoring the first and last one
rightboard = [i*N for i in range(2,N)]
# all the positions in the first row
firstrow = [i+1 for i in range(N)]
# positions to check if any of the players won the game
p1winpos = [i*N for i in range(1,N+1)]
p2winpos = [(N-1)*N+i for i in range(1,N+1)]
# all rectangles
piecesRects = []


def winGame(node, player):
    """Check if any of the players won the game."""
    if player == 'p1' and node in p1winpos:
        return True
    elif player == 'p2' and node in p2winpos:
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


def setPosition(pos, player):
    """Set the pieces for each player, then update the pieces owner per player
       and update nodes connections."""
    pieces[player].append(pos)
    # here we check if player 1 placed any piece in the left column
    if (pos-1) % N == 0 and player == 'p1':
        graph['p1'].append(pos)
    # or if the player 2 placed any piece in the first row
    if pos in firstrow and player == 'p2':
        graph['p2'].append(pos)
    if pos not in graph:
        graph[pos] = []
    checkNeighbour(pos, genNeighbour(pos), player)


def createRects():
    """Creates all rectangles we can click in the screen."""
    pieceWidth = 45
    pieceHeight = 25
    xpos = [26,48,71,94,116,139,161,184,206,228,251]
    ypos = [36,74,114,153,192,230,269,308,346,389,425]

    n = 0
    for i in range(N*N):
        if (i % N) == 0 and i != 0:
            n += 1
        piecesRects.append(Pieces(xpos[n] + (i % N)*pieceWidth, ypos[n],
                                  pieceWidth, pieceHeight, i+1))


def checkCollision(x,y, player):
    """Check if we click in a valid position in the board"""
    for r in piecesRects:
        if (r.x <= x <= r.x + r.w and
            r.y <= y <= r.y + r.h and r.clickable):
            r.clickable = False
            r.setImage(player)
            setPosition(r.pos, player)
            return True
    return False


def render(game):
    """Render all our graphics"""
    game.window.blit(game.board, (0,0))
    for r in piecesRects:
        if not r.clickable:
            game.window.blit(r.getImage(), (r.x-8, r.y-22))
    if game.end:
        game.window.blit(game.winner, (230,180))
    pygame.display.update()


def endTurn(x, y, game):
    """Change player after placing a piece"""
    if checkCollision(x,y,game.player):
        for n in graph[game.player]:
            if dfs(n, game.player):
                game.ending()
            break
        game.changePlayer()


def userInputs(game):
    """Get all user inputs"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and not game.end:
            x,y = pygame.mouse.get_pos()
            endTurn(x, y, game)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.quit()
                break
            if event.key == pygame.K_RETURN and game.end:
                game.quit()
                break


def Hex():
    """Our hex game function!!!"""
    pygame.init()
    pygame.display.set_caption("Hex")

    window = pygame.display.set_mode(screenSize)
    board = pygame.image.load("board.png").convert_alpha()

    game = Game(window, board)

    createRects()

    while game.running:
        userInputs(game)
        render(game)
    pygame.quit()


Hex()
