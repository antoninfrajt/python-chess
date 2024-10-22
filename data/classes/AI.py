import pygame
import numpy as np

from data.classes.Board import Board
#class to create funcion for AI move
class AI:
    def __init__(self,table,boards):
        self.table = table
        self.boards = boards
        
    # it works almost the same way as in the training proces but we just evaluate only black turn and we are using only the max q value action
    def do_ai_move(self,board):
        pocet_desek = len(self.boards)
        chyba = False
        obs = Board(700,700)
        obs.get_info(board)  
        obs.turn = board.turn
        for square in obs.squares:
            if square.occupying_piece is not None:  
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
        for b in self.boards:
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
                print("mame")
                obs = b
                board_num = b.number
                need_new = False
        if need_new:
            #print("novy")
            all_moves = []
            obs.number = pocet_desek
            pocet_desek += 1
            board_num = obs.number
            #print(board_num)
            all_moves.clear()
            for square in obs.squares:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == "friend":
                        obs.turn = "eny"
                        piece = square.occupying_piece
                        #print(piece.notation)
                        obs.selected_piece = piece
                        moves = []
                        for move in obs.selected_piece.get_valid_moves(obs):
                            all_moves.append((((piece.x,piece.y),piece.notation),(move.x,move.y)))
                        #print(piece)
                        #print(moves)
            #print(all_moves)
            self.boards.append(obs)
            self.table [(obs.number)] = {}
            for move in all_moves:
                self.table [(obs.number)] [move]= np.random.uniform(-5,0)
        print(board_num)
        actions = list(self.table[board_num].keys())
        action = actions[np.argmax(list(self.table[board_num].values()))]
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