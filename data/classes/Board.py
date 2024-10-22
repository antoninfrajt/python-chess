import pygame

from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn

class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.square_width = width // 8
		self.square_height = height // 8
		self.selected_piece = None
		self.turn = 'white'
		self.number = None
		self.config = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b '],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w '],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]

		self.squares = self.generate_squares()

		self.setup_board()
	def __eq__(self,other):
		same = True
		for square in self.squares:
			found = False
			for square2 in other.squares:
				if square.pos == square2.pos:
					if square.occupying_piece == square2.occupying_piece:
						found = True
				if found:
					# print("ANO")
					# print(square.occupying_piece)
					# print(square.pos)
					# print(square2.occupying_piece)
					# print(square2.pos)
					break
			if found == False:
				# print("NE")
				# print(square.occupying_piece)
				# print(square.pos)
				same = False
		#if same:
			#print("stejne")
		return same

	def get_info(self,other):
		self.squares.clear()
		for square in other.squares:
			new_square = Square(square.x,square.y,square.width,square.height)
			if square.occupying_piece is not None:
				if square.occupying_piece.notation == " ":
					new_piece = Pawn(new_square.pos,square.occupying_piece.color,self)
					new_piece.has_moved = square.occupying_piece.has_moved
					new_square.occupying_piece = new_piece
				elif square.occupying_piece.notation == "R":
					new_piece = Rook(new_square.pos,square.occupying_piece.color,self)
					new_piece.has_moved = square.occupying_piece.has_moved
					new_square.occupying_piece = new_piece
				elif square.occupying_piece.notation == "N":
					new_piece = Knight(new_square.pos,square.occupying_piece.color,self)
					new_piece.has_moved = square.occupying_piece.has_moved
					new_square.occupying_piece = new_piece
				elif square.occupying_piece.notation == "B":
					new_piece = Bishop(new_square.pos,square.occupying_piece.color,self)
					new_piece.has_moved = square.occupying_piece.has_moved
					new_square.occupying_piece = new_piece
				elif square.occupying_piece.notation == "Q":
					new_piece = Queen(new_square.pos,square.occupying_piece.color,self)
					new_piece.has_moved = square.occupying_piece.has_moved
					new_square.occupying_piece = new_piece
				elif square.occupying_piece.notation == "K":
					new_piece = King(new_square.pos,square.occupying_piece.color,self)
					new_piece.has_moved = square.occupying_piece.has_moved
					new_square.occupying_piece = new_piece
			self.squares.append(new_square)
	def save_board(self):
		new_squares = []
		for square in self.squares:
			pos = square.pos
			piece = square.occupying_piece
			if piece is not None:
				notation = piece.notation
				color = piece.color
			if piece is None:
				new_squares.append([pos,0,0])
			else:
				new_squares.append([pos,notation,color])
		return new_squares
	def load_board(self,list,number):
		self.number = number
		self.squares.clear()
		for pos,notation,color in list:
			new_square = Square(pos[0],pos[1],self.square_width,self.square_height)
			if notation != 0:
				if notation == " ":
					new_piece = Pawn(new_square.pos,color,self)
					new_square.occupying_piece = new_piece
				elif notation == "R":
					new_piece = Rook(new_square.pos,color,self)
					new_square.occupying_piece = new_piece
				elif notation == "N":
					new_piece = Knight(new_square.pos,color,self)
					new_square.occupying_piece = new_piece
				elif notation == "B":
					new_piece = Bishop(new_square.pos,color,self)
					new_square.occupying_piece = new_piece
				elif notation == "Q":
					new_piece = Queen(new_square.pos,color,self)
					new_square.occupying_piece = new_piece
				elif notation == "K":
					new_piece = King(new_square.pos,color,self)
					new_square.occupying_piece = new_piece
			self.squares.append(new_square)
		
	def generate_squares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(
						x,
						y,
						self.square_width,
						self.square_height
					)
				)

		return output


	def setup_board(self):
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))

					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == ' ':
						square.occupying_piece = Pawn(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)


	def handle_click(self, mx, my):
		x = mx // self.square_width
		y = my // self.square_height
		clicked_square = self.get_square_from_pos((x, y))

		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece

		elif self.selected_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'

		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				self.selected_piece = clicked_square.occupying_piece

	def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K':
					if piece.color == color:
						king_pos = piece.pos
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
						
		return output


	def is_in_checkmate(self, color):
		output = False
		king = None

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if piece.notation == 'K' and piece.color == color:
					king = piece
			if king is not None:
				if king.get_valid_moves(self) == []:
					if self.is_in_check(color):
						output = True
		else:
			output = False

		return output

	def is_in_pat(self, color):
		output = False 
		pieces = []

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if piece.color == color:
					pieces.append(piece)
		if len(pieces) == 1:
			king = pieces[0]
			if king.get_valid_moves(self) == []:
				if self.is_in_check(color)==False:
					output = True
		return output			

	def get_square_from_pos(self, pos):
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square
		

	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece


	def draw(self, display):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)