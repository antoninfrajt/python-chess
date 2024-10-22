import numpy as np
import pickle
import matplotlib.pyplot as plt
import time
from matplotlib import style

from data.classes.Board import Board
import pygame

# some starting constants

WINDOW_SIZE = (700, 700)
style.use("ggplot")
pygame.init
screen = pygame.display.set_mode(WINDOW_SIZE)
def draw(display):
	display.fill("white")

	board.draw(display)

	pygame.display.update()
board = Board(WINDOW_SIZE[0],WINDOW_SIZE[1])
all_boards = []
PIECE_VALUE = { " ":1,
                "B":3,
                "N":3,
                 "R":5,
                  "Q":9 }
CHECK_REWARD = 10000
epsilon = 0.5
EPS_DECAY = 0.999
SHOW_EVERY = 100
pocet_desek = 0
done = False
start_q_table = "qtable-171288881540overnight.pickle"
boards_save = "boards-171288881640overnight.pickle"
q_table = {}
HM_EPISODES = 80
LEARNING_RATE = 0.1
DISCOUNT = 0.95
all_moves = []

#there we look if we have defined q_table and if not we create a new q_table
#also i desided to go for dynamic q_table bcs there is a lot of posible board states in this game

if start_q_table is None:
    start_board = Board(WINDOW_SIZE[0],WINDOW_SIZE[1])
    start_board.get_info(board)
    start_board.turn = board.turn
    start_board.number = pocet_desek 
    pocet_desek += 1
    all_moves = []

    # there we are fliping the board so it looks same for white and black player

    for square in start_board.squares:
        if square.occupying_piece is not None:  
            if start_board.turn == "white":
                if square.occupying_piece.color == "white":
                    square.occupying_piece.color = "friend"
                elif square.occupying_piece.color == "black": 
                    square.occupying_piece.color = "eny"
            if start_board.turn == "black":
                if square.occupying_piece.color == "black":
                    square.occupying_piece.color = "friend"
                elif square.occupying_piece.color == "white": 
                    square.occupying_piece.color = "eny"
                #print(square.occupying_piece.notation)
                #print(square.x,square.y)
                square.x = 7-square.x
                square.y = 7-square.y
                square.occupying_piece.x = 7-square.occupying_piece.x
                square.occupying_piece.y = 7-square.occupying_piece.y
                #print(square.x,square.y)
    #print(board.squares[2].occupying_piece.color)            
    for square in start_board.squares:
        if square.occupying_piece is not None:
            if square.occupying_piece.color == "friend":
                start_board.turn = "friend"
                piece = square.occupying_piece
                #print(piece.notation)
                start_board.selected_piece = piece
                moves = []
                for move in start_board.selected_piece.get_valid_moves(start_board):
                    all_moves.append((((piece.x,piece.y),piece.notation),(move.x,move.y)))
                #print(piece)
                #print(moves)
    all_boards.append(start_board)
    start_board.turn = board.turn
    #print(all_moves)
    q_table [(start_board.number)] = {}
    for move in all_moves:
        q_table [(start_board.number)] [move]= np.random.uniform(-5,0)

# if we have defined q_table at the start we just open the file with it

else:
    with open(start_q_table, "rb") as file:
        q_table = pickle.load(file)
with open(boards_save, "rb") as file:
	boards_save = pickle.load(file)
for bo in boards_save:
	b = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
	b.load_board(bo,boards_save.index(bo))
	all_boards.append(b)
episode_rewards = []

# loop for one game of chess with defined number of turns

for episode in range(HM_EPISODES):
    print(episode)
    if episode % SHOW_EVERY == 0:
        show = True
    else:
        show = False
    episode_reward = 0
    if show:
        screen = pygame.display.set_mode(WINDOW_SIZE)
    board = Board(WINDOW_SIZE[0],WINDOW_SIZE[1])
    done = False
    turn = 0

    # loop for one turn

    while done == False:
        chyba = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if show:
            draw(screen)
        turn+=1
        if turn % 50 == 0:
            print(turn)
        #board_num = 1

        # geting obs (observation space)

        obs = Board(WINDOW_SIZE[0],WINDOW_SIZE[1])
        obs.get_info(board)  
        obs.turn = board.turn
        
        #fliping board again

        for square in obs.squares:
            if square.occupying_piece is not None:  
                if obs.turn == "white":
                    if square.occupying_piece.color == "white":
                        square.occupying_piece.color = "friend"
                    elif square.occupying_piece.color == "black": 
                        square.occupying_piece.color = "eny"
                if obs.turn == "black":
                    if square.occupying_piece.color == "black":
                        square.occupying_piece.color = "friend"
                    elif square.occupying_piece.color == "white": 
                        square.occupying_piece.color = "eny"
                    #print(square.occupying_piece.notation)
                    #print(square.x,square.y)
                    square.y = 7-square.y
                    square.occupying_piece.y = 7-square.occupying_piece.y
                    #print(square.x,square.y)
            else:
                if obs.turn == "black":
                    square.y = 7-square.y
        need_new = True
        #print(all_boards)

        #here we go through all boards we already have in our q_table
        # and we want to find which board we now have in our obs
    
        for b in all_boards:
            if b == obs:
                # print(b)
                # print(b.number)
                # for square in b.squares:
                #     print(square.pos,square.occupying_piece)
                #     if square.occupying_piece is not  None:
                #         print(square.occupying_piece.color)
                # print(obs)
                # print(obs.number)
                # for square in obs.squares:
                #     print(square.pos,square.occupying_piece)
                #     if square.occupying_piece is not  None:
                #             print(square.occupying_piece.color)
                #print("mame")
                obs = b
                board_num = b.number
                need_new = False
        #print(pocet)

        #deciding function
        #we take random value or the value with highest q

        if np.random.random() > epsilon:
            #print("nerandom")
            actions = list(q_table[board_num].keys())
            action = actions[np.argmax(list(q_table[board_num].values()))]
        else:
            #print(board_num)
            actions = list(q_table[board_num].keys())
            action = actions[np.random.randint(0,len(actions))]
        #print("ahoj")
        #print(action)
        last_move = None
        
        #getting the action played on our gameboard

        if board.turn == "white":
            #white move

            board.selected_piece = board.get_piece_from_pos(action[0][0])
            #print(action[1])
            #print(board.selected_piece)
            if board.selected_piece is None:
                print("chyba")
                chyba = True
            #print(board.selected_piece.notation)
            #print(board.get_square_from_pos(action[1]).x,board.get_square_from_pos(action[1]).y)
            if chyba == False:
                board.selected_piece.move(board,board.get_square_from_pos(action[1]))
            prev_square = action[0][0]
            act_square = action[1]
            #print(prev_square)
            #print(board.get_piece_from_pos(prev_square))
            #print(act_square)
            #print(board.get_piece_from_pos(act_square))
            board.turn = "black"
            last_move = act_square
        else:
            #black move

            black_action = tuple(((action[0][0][0],7-action[0][0][1]),(action[1][0],7-action[1][1])))
            board.selected_piece = board.get_piece_from_pos(black_action[0])
            if board.selected_piece is None:
                print("chyba")
                chyba = True
            #print(black_action)
            #print(board.selected_piece.notation)
            if chyba == False:
                board.selected_piece.move(board,board.get_square_from_pos(black_action[1]))
            prev_square = black_action[0]
            act_square = black_action[1]
            #print(prev_square)
            #print(board.get_piece_from_pos(black_action[0]))
            #print(act_square)
            #print(board.get_piece_from_pos(black_action[1]))
            board.turn = "white"
            last_move = [prev_square,act_square]
        #if we try to move with figure that doesnt exist we end the game

        if chyba:
            new_q = -100000
            q_table[board_num][action] = new_q
            done = True
            break
        reward = 0
        #counting our reward

        for square in board.squares:
            if square.occupying_piece is not None:
                #print(square.occupying_piece.color)
                if square.occupying_piece.color == "friend":
                    #print(square.occupying_piece.notation)
                    if square.occupying_piece.notation != "K":
                        reward += PIECE_VALUE[square.occupying_piece.notation]*100
                elif square.occupying_piece.color == "eny":
                    if square.occupying_piece.notation != "K":
                        reward -= PIECE_VALUE[square.occupying_piece.notation]*100
        #getting obs after the turn is played

        new_obs = Board(WINDOW_SIZE[0],WINDOW_SIZE[1])
        new_obs.get_info(board)  
        new_obs.turn = board.turn

        #fliping board again

        for square in new_obs.squares:
            if square.occupying_piece is not None:  
                if new_obs.turn == "white":
                    if square.occupying_piece.color == "white":
                        square.occupying_piece.color = "friend"
                    elif square.occupying_piece.color == "black": 
                        square.occupying_piece.color = "eny"
                if new_obs.turn == "black":
                    if square.occupying_piece.color == "black":
                        square.occupying_piece.color = "friend"
                    elif square.occupying_piece.color == "white": 
                        square.occupying_piece.color = "eny"
                    #print(square.occupying_piece.notation)
                    #print(square.x,square.y)
                    square.y = 7-square.y
                    square.occupying_piece.y = 7-square.occupying_piece.y
                    #print(square.x,square.y)
            else:
                if new_obs.turn == "black":
                    square.y = 7-square.y
        need_new = True
        #print(all_boards)

        # looking into q_table if we havent seen this board yet
        # if we have it in our q_table just get q values 
        for b in all_boards:
            if b == new_obs:
                # print(b)
                # print(b.number)
                # for square in b.squares:
                #     print(square.pos,square.occupying_piece)
                #     if square.occupying_piece is not  None:
                #         print(square.occupying_piece.color)
                # print(new_obs)
                # print(new_obs.number)
                # for square in new_obs.squares:
                #     print(square.pos,square.occupying_piece)
                #     if square.occupying_piece is not  None:
                #             print(square.occupying_piece.color)
                #print("mame")
                new_obs = b
                new_board_num = b.number
                need_new = False
        #print(pocet)
        # if not we have to create new q_table row with random q values
        if need_new:
            #print("novy")
            new_obs.number = pocet_desek
            pocet_desek += 1
            new_board_num = new_obs.number
            #print(board_num)
            all_moves.clear()
            for square in new_obs.squares:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == "friend":
                        new_obs.turn = "eny"
                        piece = square.occupying_piece
                        #print(piece.notation)
                        new_obs.selected_piece = piece
                        moves = []
                        for move in new_obs.selected_piece.get_valid_moves(new_obs):
                            all_moves.append((((piece.x,piece.y),piece.notation),(move.x,move.y)))
                        #print(piece)
                        #print(moves)
            #print(all_moves)
            all_boards.append(new_obs)
            q_table [(new_obs.number)] = {}
            for move in all_moves:
                q_table [(new_obs.number)] [move]= np.random.uniform(-5,0)
        else:
            all_moves.clear()
            for square in new_obs.squares:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == "friend":
                        new_obs.turn = "friend"
                        piece = square.occupying_piece
                        #print(piece.notation)
                        new_obs.selected_piece = piece
                        moves = []
                        for move in new_obs.selected_piece.get_valid_moves(new_obs):
                            all_moves.append((((piece.x,piece.y),piece.notation),(move.x,move.y)))
                        #print(piece)
                        #print(moves)
            #print(all_moves)

        # for friendly piece you get points for every enemy piece you lose points so we can find the diference
        for square in new_obs.squares:
            if square.occupying_piece is not None:
                #print(square.occupying_piece.color)
                if square.occupying_piece.color == "eny":
                    #print(square.occupying_piece.notation)
                    if square.occupying_piece.notation != "K":
                        reward += PIECE_VALUE[square.occupying_piece.notation]*100
                        # print(square.occupying_piece.notation,"+",PIECE_VALUE[square.occupying_piece.notation]*100)
                        # print(reward)
                elif square.occupying_piece.color == "friend":
                    if square.occupying_piece.notation != "K":
                        reward -= PIECE_VALUE[square.occupying_piece.notation]*100
                        # print(square.occupying_piece.notation,"-",PIECE_VALUE[square.occupying_piece.notation]*100)
                        # print(reward)
        # here i just gave small reward for creating boards with more moves
        for i in all_moves:
            reward += 1
        # reward for checking enemy
        if board.is_in_check(board.turn):
            reward += CHECK_REWARD
        if len(list(q_table[new_board_num].values()))!= 0:
        # defining next max q value for our q function
            max_future_q = np.max(list(q_table[new_board_num].values()))
        else:
            max_future_q = 0
        current_q = q_table[board_num][action]
        if reward == CHECK_REWARD:
            new_q = CHECK_REWARD
        # checkmate outcome
        elif board.is_in_checkmate(board.turn):
            reward = 100000
            new_q = reward
            barvy = ["white","black"]
            for barva in barvy:
                if barva != board.turn:
                    print(barva+"wins")
            draw(screen)
            time.sleep(2)
            done = True
        # pat outcome
        elif board.is_in_pat(board.turn) or len(all_moves) == 0:
            reward = -50000
            new_q = reward
            print("Draw")
            draw(screen)
            time.sleep(2)
            done = True
        # here we stop our loop and save q value if we exceed turn limit
        elif turn >= 50:
            new_q = reward
            print("konec")
            #draw(screen)
            #print(reward)
            time.sleep(2)
            done = True
        else:
        # Q FUNCTION
            new_q = (1-LEARNING_RATE)* current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[board_num][action] = new_q
        #print("reward:") 
        #print(reward)
        # drawing a board if we can
        if show:
            draw(screen)
        if turn % 2 == 0:
            episode_reward += reward
    # getting episode reward for our graph
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY
    # saving q_table more often than just on the end of program
    if episode % 20 == 0 and episode != 0:
        with open(f"qtable-{int(time.time())}{40+episode}games.pickle", "wb") as f:
            pickle.dump(q_table, f)
        all_boards_saved = []
        for bo in all_boards:
            all_boards_saved.append(bo.save_board())
#print(all_boards_saved)
        with open(f"boards-{int(time.time())}{40+episode}games.pickle", "wb") as f:
            pickle.dump(all_boards_saved, f)
    if show:
        print("episode:",episode)
        print("reward:",episode_reward)

# printing graph
moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

# final saving of our q_table 
with open(f"qtable-{int(time.time())}overnight.pickle", "wb") as f:
    pickle.dump(q_table, f)
all_boards_saved = []
# here i had to display all boards in one list to be able to save then in pickle format
for bo in all_boards:
    all_boards_saved.append(bo.save_board())
#print(all_boards_saved)
with open(f"boards-{int(time.time())}overnight.pickle", "wb") as f:
    pickle.dump(all_boards_saved, f)

# for square in board.squares:
#     print(square.pos,square.occupying_piece)
#     if square.occupying_piece is not  None:
#         print(square.occupying_piece.color)
#print(all_boards)
# for n in q_table.keys():
#     print(n)
#     print(q_table[n])

        





