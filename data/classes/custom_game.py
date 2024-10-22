import pygame
from data.classes.Board import Board

import gymnasium as gym
class custom_game(gym.Env):
    def __init__(self,grid_size):
        pygame.init()

        WINDOW_SIZE = (700, 700)
        screen = pygame.display.set_mode(WINDOW_SIZE)

        board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

        def draw(display):
            display.fill('white')

            board.draw(display)

            pygame.display.update()


        running = True
        while running:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        board.handle_click(mx, my)
            draw(screen)
        tahy = []
        for i in Board.squares:
            if i.occupying_piece != None:
                if i.occupying_piece.color == Board.turn:
                    tahy.append(i)                    
        self.action_space = tahy
        self.observation_space = Board.squares
    def _get_obs(self):
        self.observation_space = Board.squares
    def reset(self):
        Board.setup_board
        tahy = []
        for i in Board.squares:
            if i.occupying_piece != None:
                if i.occupying_piece.color == Board.turn:
                    tahy.append(i)                    
        self.action_space = tahy
        self.observation_space = Board.squares
        return self._get_obs
    def step(self,action):
        