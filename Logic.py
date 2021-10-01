for i in range(3) : print('\n')

import pygame, sys

is_game_over = False
game_turn = True

BOARD_SIZE = 12
SQUARE_SIZE = 60
BORDER = int( SQUARE_SIZE * 0.2 )
PIECE_SIZE = int( SQUARE_SIZE * 0.8 )

# Colors
LIGHT_SQ = (220, 220, 230)
DARK_SQ = (127, 127, 255)
YELLOW = (255, 255, 127)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption('Real Chess Game')
# pygame.display.set_icon( pygame.image.load('Icon.jpg') )
chess_font = pygame.font.SysFont('Chess', PIECE_SIZE)

SCREEN_SIZE = (BOARD_SIZE - 4) * SQUARE_SIZE + BORDER * 2
screen = pygame.display.set_mode( (SCREEN_SIZE, SCREEN_SIZE) )

get_sqr_bgcolor = lambda pos: (LIGHT_SQ, DARK_SQ)[(pos[0] + pos[1]) % 2]

class Coordinate:
	def __init__( self, tup ):
		self.update_coords(tup)

	def update_coords( self, tup ):
		self.ind_r, self.ind_c = self.index = tup

	centered = lambda self, ind: ind * SQUARE_SIZE + int((SQUARE_SIZE - PIECE_SIZE) / 2) + BORDER 

	@property
	def coords( self ):
		return ( self.centered(self.ind_c), self.centered(self.ind_r) )

sqr_from = Coordinate( (None, None) )
sqr_to = Coordinate( (None, None) )

class Board:
	position = ['~' * 12] * 2 + ['~~rnbqkbnr~~','~~0pp00ppp~~'] + ['~~00000000~~'] * 4 + ['~~0PPP0P0P~~','~~RNBQKBNR~~'] + ['~' * 12] * 2

	piece_obj = [[None] * 8 for _ in range(8)]

	@staticmethod
	def draw_squares():
		for r in range(BOARD_SIZE - 4):
			for c in range(BOARD_SIZE - 4):
				square = (r * SQUARE_SIZE + BORDER, c * SQUARE_SIZE + BORDER, SQUARE_SIZE, SQUARE_SIZE)
				pygame.draw.rect(screen, get_sqr_bgcolor( (r, c) ), square)

	@staticmethod
	def set_position():
		for r in range(BOARD_SIZE - 4):
			for c in range(BOARD_SIZE - 4):
				piece = Board.position[r + 2][c + 2]
				
				if piece.isalpha():
					Board.piece_obj[r][c] = Piece.get_class( piece )
					Piece.draw ( Coordinate((r, c)), piece )
				# elif piece == '0':

		pygame.display.flip()

	@staticmethod
	def update_position( sqr, p ):
		Board.position[sqr.ind_r + 2] = Board.position[sqr.ind_r + 2][: sqr.ind_c + 2] + ('0' if p == ' ' else p) + Board.position[sqr.ind_r + 2][sqr.ind_c + 3 :]

class Piece:
	homes = []
	@staticmethod
	def get_class( piece_ch ):
		return { 'P': Pawn, 'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King } [piece_ch.upper()]()

	@staticmethod
	def draw( ind, piece_sym, to_update_board_position = True ):
		label = chess_font.render(piece_sym, True, BLACK, get_sqr_bgcolor( ind.index ))
		screen.blit( label, ind.coords )

		if to_update_board_position:
			Board.update_position( ind, piece_sym )
		
	@staticmethod
	def move( indices ):
		sqr_to.update_coords( indices )

		get_piece_from = lambda idx: Board.position[idx.ind_r + 2][idx.ind_c + 2]
		global sqr_from, is_selected, game_turn

		print(sqr_to.index)
		piece = get_piece_from( sqr_to )

		if piece.isupper() if game_turn else piece.islower():	# First Click
			Board.piece_obj[sqr_to.ind_r][sqr_to.ind_c].show_path()
			sqr_from.update_coords( sqr_to.index )
			is_selected = True

		elif is_selected and sqr_to.index in Piece.homes:
			piece = get_piece_from( sqr_from )

			Piece.draw( sqr_from, ' ' )	# delete piece
			Piece.draw( sqr_to, piece )	# add to new index

			Board.piece_obj[sqr_to.ind_r][sqr_to.ind_c] = Board.piece_obj[sqr_from.ind_r][sqr_from.ind_c]
			Board.piece_obj[sqr_from.ind_r][sqr_from.ind_c] = None

			Piece.homes.remove(sqr_to.index)
			for home in Piece.homes:
				Piece.draw( Coordinate(home), ' ', False )
			
			Piece.homes.clear()
			is_selected = False
			game_turn = not game_turn	# Switching Turn
		
	@staticmethod
	def calculate_path(direction, to_continue = True):
		current_sqr = ()
		for d in direction:
			current_sqr = (sqr_to.ind_r + d[0], sqr_to.ind_c + d[1])
			while Board.position[current_sqr[0] + 2][current_sqr[1] + 2] == '0':
				Piece.homes.append(current_sqr)
				Piece.draw( Coordinate(current_sqr), 'o', False )
				if to_continue:
					current_sqr = (current_sqr[0] + d[0], current_sqr[1] + d[1])
				else:
					break

class Pawn:
	can_double_move = True
	# @staticmethod
	def show_path(self):
		pass

class Knight:
	def show_path(self):
		Piece.calculate_path( [(-1, -2), (-2, -1), (-2, 1), (1, -2), (1, 2), (2, 1), (2, -1), (-1, 2)], False )

class Bishop:
	def show_path(self):
		Piece.calculate_path( [(-1, -1), (-1, 1), (1, 1), (1, -1)] )

class Rook:
	def show_path(self):
		Piece.calculate_path( [(-1, 0), (0, 1), (1, 0), (0, -1)] )

class Queen:
	def show_path(self):
		Piece.calculate_path( [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)] )

class King:
	def show_path(self):
		Piece.calculate_path( [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)], False )


Board.draw_squares()
Board.set_position()

while not is_game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print(*Board.position[2:-2], sep='\n')
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if not (BORDER < event.pos[0] < SCREEN_SIZE - BORDER and BORDER < event.pos[1] < SCREEN_SIZE - BORDER):
				continue

			indices = tuple( int((n - BORDER) / SQUARE_SIZE) for n in event.pos )
			# print(indices, event.pos)

			Piece.move( indices[::-1] )

			pygame.display.update()
			
			
			
			# aditya
			
			# Python program to check if year is a leap year or not

year = 2000

# To get year (integer input) from the user
# year = int(input("Enter a year: "))

if (year % 4) == 0:
   if (year % 100) == 0:
       if (year % 400) == 0:
           print("{0} is a leap year".format(year))
       else:
           print("{0} is not a leap year".format(year))
   else:
       print("{0} is a leap year".format(year))
else:
   print("{0} is not a leap year".format(year))
