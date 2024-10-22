import pygame
import pickle

from data.classes.Board import Board
from data.classes.AI import AI


pygame.init()
# setting important constants
WINDOW_SIZE = (700, 700)
screen = pygame.display.set_mode(WINDOW_SIZE)
q_table = "qtable-171288276520overnight.pickle"
with open(q_table, "rb") as file:
    q_table = pickle.load(file)
for n in q_table.keys():
    print(n)
    print(q_table[n])
boards = []
boards_save = "boards-171288276620overnight.pickle"
with open(boards_save, "rb") as file:
	boards_save = pickle.load(file)
#print(boards_save)
deska = 1
maximum = len(boards_save)
#print(maximum)
# creating list of Board class objects so i can use it in AI turn
for bo in boards_save:
	b = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
	b.load_board(bo,boards_save.index(bo))
	deska+= 1
	boards.append(b)
	#print(str(deska)+" z "+str(maximum))
	#print(str((deska/maximum)*100) + "%")
#print(boards)
#creating the game itself
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
Adam = AI(q_table,boards)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

def draw(display):
	display.fill("white")

	board.draw(display)

	pygame.display.update()


running = True
while running:
	can_play = True
	draw(screen)
	mx, my = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		#game accepts the mouse click only when it is white turn
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1 and board.turn == "white":
				board.handle_click(mx, my)

	if board.is_in_checkmate('black'):
		can_play = False
		print('White wins!')
		running = False
	elif board.is_in_checkmate('white'):
		print('Black wins!')
		running = False
	elif board.is_in_pat('black') or board.is_in_pat('white'):
		print('Draw')
		running = False
	# if there is no reason for game to be ended black (AI) plays its move
	if board.turn == "black" and can_play:
		Adam.do_ai_move(board)
	draw(screen)