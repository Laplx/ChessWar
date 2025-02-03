import pygame
import Piece

class ChessBoard:
    def __init__(self):
        self.size = 8
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.initialize()

    def initialize(self):
        self.board[0][4] = Piece.King(1)
        self.board[7][4] = Piece.King(0)
        self.playing_color = 0
        self.tokens = [2, 2]
        
    def draw(self, pieces, screen, font):
            colors = [(135, 206, 250), (72, 61, 139)]
            for row in range(self.size):
                for col in range(self.size):
                    color = colors[(row + col) % 2]
                    pygame.draw.rect(screen, color, (col * 80, row * 80, 80, 80))
                    piece = self.board[row][col]
                    if piece is not None:
                        piece.draw(pieces, screen, font, col * 80, row * 80)
                        
    def move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece.is_valid_move(start_row, start_col, end_row, end_col, self.board):
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            return True
        return False
    
    def attack(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece.is_valid_attack(start_row, start_col, end_row, end_col, self.board):
            self.board[end_row][end_col].hp -= piece.ad
            if self.board[end_row][end_col].hp > 100:
                self.board[end_row][end_col].hp = 100
            elif self.board[end_row][end_col].hp <= 0:
                self.board[end_row][end_col] = None
            return True
        return False
    
    def buy(self, piece_type, row, col):
        origin = self.tokens[self.playing_color]
        if piece_type == "Pawn":
            self.tokens[self.playing_color] -= 2
            new_piece = Piece.Pawn(self.playing_color)
        elif piece_type == "Rook":
            self.tokens[self.playing_color] -= 3
            new_piece = Piece.Rook(self.playing_color)
        elif piece_type == "Knight":
            self.tokens[self.playing_color] -= 3
            new_piece = Piece.Knight(self.playing_color)
        elif piece_type == "Bishop":
            self.tokens[self.playing_color] -= 4
            new_piece = Piece.Bishop(self.playing_color)
        elif piece_type == "Queen":
            self.tokens[self.playing_color] -= 4
            new_piece = Piece.Queen(self.playing_color)
        
        if self.tokens[self.playing_color] >= 0 and new_piece.is_valid_born(row, col, self.board):
            self.board[row][col] = new_piece
            return True
        else:
            self.tokens[self.playing_color] = origin
            return False