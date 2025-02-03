import pygame

class Piece:   
    def __init__(self, color):
        self.color = color # 0 for white and 1 for black
        self.hp = 0
        self.ad = 0
        self.move_directions = []
        self.attack_directions = []

    def draw(self, pieces, screen, font, x, y):
        screen.blit(pieces[self.__class__.__name__][self.color], (x, y))
        text_hp = font.render(f"HP:{self.hp}", True, (255, 255, 255))
        text_ad = font.render(f"AD:{self.ad}", True, (255, 255, 255))
        screen.blit(text_hp, (x + 20, y + 20))
        screen.blit(text_ad, (x + 20, y + 40))
        
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        if end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8:
            return False
        if board[end_row][end_col] is not None:
            return False
        return (end_row, end_col) in self.get_moves(board, start_row, start_col)

    def is_valid_attack(self, start_row, start_col, end_row, end_col, board):
        if end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8:
            return False
        if board[end_row][end_col] is None or board[end_row][end_col].color == self.color:
            return False
        return (end_row, end_col) in self.get_attacks(board, start_row, start_col)
    
    def is_valid_born(self, row, col, board):
        if row < 0 or row >= 8 or col < 0 or col >= 8:
            return False
        if board[row][col] is not None:
            return False
        return True
    
    def get_moves(self, board, row, col):
        moves = []
        for dr, dc in self.move_directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                moves.append((new_row, new_col))
        return moves
    
    def get_attacks(self, board, row, col):
        attackees = []
        for dr, dc in self.attack_directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                attackees.append((new_row, new_col))
        return attackees


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hp = 100
        self.ad = 10
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]        
    
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hp = 24
        self.ad = 100
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
    def is_valid_born(self, row, col, board):
        if super().is_valid_born(row, col, board):
            born_position = [(0, 3), (0, 4)] if self.color else [(7, 3), (7, 4)]
            return (row, col) in born_position
        return False
        
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hp = 15
        self.ad = 5
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def is_valid_born(self, row, col, board):
        if super().is_valid_born(row, col, board):
            if row == 1 and self.color == 1:
                return True
            elif row == 6 and self.color == 0:
                return True
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hp = 12
        self.ad = 4
        
    def get_moves(self, board, row, col):
        moves = []
        size = len(board)
        for dr in range(1, size):
            new_row, new_col = row + dr, col
            self.flag_pos_r = dr
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        for dr in range(-1, - size, -1):
            new_row, new_col = row + dr, col
            self.flag_neg_r = dr
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        for dc in range(1, size):
            new_row, new_col = row, col + dc
            self.flag_pos_c = dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        for dc in range(-1, - size, -1):
            new_row, new_col = row, col + dc
            self.flag_neg_c = dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        return moves
    
    def get_attacks(self, board, row, col):
        self.get_moves(board, row, col)
        attackees = [(row + self.flag_pos_r, col), (row + self.flag_neg_r, col),
                     (row, col + self.flag_pos_c), (row, col + self.flag_neg_c)]
        return attackees
    
    def is_valid_born(self, row, col, board):
        if super().is_valid_born(row, col, board):
            born_position = [(0, 0), (0, 7)] if self.color else [(7, 0), (7, 7)]
            return (row, col) in born_position
        return False
    
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hp = 24
        self.ad = 7
        self.move_directions = [(1, 2), (-1, 2), (-1, -2), (1, -2), (2, 1), (2, -1), (-2, -1), (-2, 1)]
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),
                                  (0, 2), (1, 2), (-1, 2), (0, -2), (1, -2), (-1, -2),
                                  (2, 0), (2, 1), (2, -1), (-2, 0), (-2, 1), (-2, -1)]  
    def is_valid_born(self, row, col, board):
       if super().is_valid_born(row, col, board):
           born_position = [(0, 1), (0, 6)] if self.color else [(7, 1), (7, 6)]
           return (row, col) in born_position
       return False
   
    def get_attacks(self, board, row, col):
        # the first blocks the next three
        attackees = super().get_attacks(board, row, col)
        group = [[(0, 1), [(0, 2), (1, 2), (-1, 2)]], [(0, -1), [(0, -2), (1, -2), (-1, -2)]],
                 [(1, 0), [(2, 0), (2, 1), (2, -1)]], [(-1, 0), [(-2, 0), (-2, 1), (-2, -1)]]]
        for blocker, blockees in group:
            dr, dc = blocker
            new_row, new_col = row + dr, col + dc
            new_blockees = []
            for dr, dc in blockees:
                new_blockees.append((row + dr, col + dc))
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    attackees = [_ for _ in attackees if _ not in new_blockees]
        return attackees
     
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hp = 36
        self.ad = -4 # heal other pieces
        
    def get_moves(self, board, row, col):
        moves = []
        size = len(board)
        for dr in range(1, size):
            new_row, new_col = row + dr, col - dr
            self.flag_pos_r = dr
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        for dr in range(-1, - size, -1):
            new_row, new_col = row + dr, col - dr
            self.flag_neg_r = dr
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        for dc in range(1, size):
            new_row, new_col = row + dc, col + dc
            self.flag_pos_c = dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        for dc in range(-1, - size, -1):
            new_row, new_col = row + dc, col + dc
            self.flag_neg_c = dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is not None:
                    break
                moves.append((new_row, new_col))
        return moves
    
    def get_attacks(self, board, row, col):
        self.get_moves(board, row, col)
        attackees = [(row + self.flag_pos_r, col - self.flag_pos_r), (row + self.flag_neg_r, col - self.flag_neg_r),
                     (row + self.flag_pos_c, col + self.flag_pos_c), (row + self.flag_neg_c, col + self.flag_neg_c)]
        return attackees
    
    def is_valid_attack(self, start_row, start_col, end_row, end_col, board):
        if end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8:
            return False
        if board[end_row][end_col] is None or board[end_row][end_col].color != self.color:
            return False
        return (end_row, end_col) in self.get_attacks(board, start_row, start_col)
    
    def is_valid_born(self, row, col, board):
        if super().is_valid_born(row, col, board):
            born_position = [(0, 2), (0, 5)] if self.color else [(7, 2), (7, 5)]
            return (row, col) in born_position
        return False
    