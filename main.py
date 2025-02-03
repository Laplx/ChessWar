import asyncio, sys
import pygame
import Board, Piece


def show_message(screen, message):
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    pygame.draw.rect(screen, (0, 0, 0), (text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(1000)
    
def introduce():
    txt = '''CHESS WAR rules
    
(1) Each piece can move once and attack once, in any order.
    - Click round botton to complete actions.
    - Attack opponent's king to 0 health to win.
(2) Buy pieces and put them at starting positions as chess.
    - Players get $1 per round.
    - Queens can be put at normal king or queen squares.
(3) Queens and pawns move like king, and others remain the same.
(4) Attack range:
    - King, queen, pawn can attack its 8 adjacent squares.
    - Rook can attack the first piece along its straight lines.
    - Bishop can heal the first piece along its diagonal lines.
    - Knight can attack all squares in 2*2 distance except (+-2,+-2).
(5) Haelth and attack list:
    - HP: K 100, Q 24, P 15, B 36, N 24, R 12
    - AD: K 10, Q 100, P 5, B -4, N 7, R 4
    '''
    
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    
    intro_rect = pygame.Rect(60, 60, 520, 680)
    button_rect = pygame.Rect(270, 640, 100, 50)
    while show_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return False

        pygame.draw.rect(screen, background_color, intro_rect)

        y_offset = 80
        for line in txt.split("\n"):
            text = font.render(line, True, text_color)
            screen.blit(text, (intro_rect.x + 20, y_offset))
            y_offset += 30
            
        pygame.draw.rect(screen, (0, 0, 139), button_rect)
        button_text = font.render("Close", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 30, button_rect.y + 10))
            
        pygame.display.update()
        
    return True


async def main():
    global running, show_intro, pieces, screen, font
    
    pygame.init()
    font = pygame.font.SysFont("arial", 20)
    screen = pygame.display.set_mode((640, 800))
    clock = pygame.time.Clock()
    
    intro_button_text = font.render("Info", True, (255, 255, 255))
    # done_button_text see below
    pawn_text = font.render("Pawn$2", True, (0, 0, 0))
    rook_text = font.render("Rook$3", True, (0, 0, 0))
    knight_text = font.render("Knight$3", True, (0, 0, 0))
    bishop_text = font.render("Bishop$4", True, (0, 0, 0))
    queen_text = font.render("Queen$4", True, (0, 0, 0))
    
    intro_button_rect = pygame.Rect(480, 640, 160, 80)
    done_button_rect = pygame.Rect(480, 720, 160, 80)
    pawn_rect = pygame.Rect(0, 640, 80, 160)
    rook_rect = pygame.Rect(80, 640, 80, 160)
    knight_rect = pygame.Rect(160, 640, 80, 160)
    bishop_rect = pygame.Rect(240, 640, 80, 160)
    queen_rect = pygame.Rect(320, 640, 80, 160)
    
    pieces = {}
    for piece_type in ['Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King']:         
        pieces[piece_type] = [pygame.transform.scale(pygame.image.load(f'assets/{piece_type}{color}.png'), (80, 80)) for color in [0, 1]]
    
    chess_board = Board.ChessBoard()
    
    wanted_piece_type = None
    selected_piece = None
    moved = []
    attacked = []
    
    running = True
    show_intro = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not show_intro:
                mouse_x, mouse_y = event.pos
                col = mouse_x // 80
                row = mouse_y // 80
                
                
                if intro_button_rect.collidepoint(event.pos):
                    show_intro = True
                    introduce()
                    show_intro = False
                    break
                elif done_button_rect.collidepoint(event.pos):
                    chess_board.playing_color = 1 - chess_board.playing_color
                    chess_board.tokens[0] += 1
                    chess_board.tokens[1] += 1
                    moved = []
                    attacked = []
                    selected_piece = None
                    selected_position = None
                    wanted_piece_type = None
                    break
                
                if pawn_rect.collidepoint(event.pos):
                    wanted_piece_type = "Pawn"
                    break
                elif rook_rect.collidepoint(event.pos):
                    wanted_piece_type = "Rook"
                    break
                elif knight_rect.collidepoint(event.pos):
                    wanted_piece_type = "Knight"
                    break
                elif bishop_rect.collidepoint(event.pos):
                    wanted_piece_type = "Bishop"
                    break
                elif queen_rect.collidepoint(event.pos):
                    wanted_piece_type = "Queen"
                    break
                
                if wanted_piece_type is not None:
                    if chess_board.buy(wanted_piece_type, row, col):
                        wanted_piece_type = None                        
                    else:
                        show_message(screen, 'Not Allowed')
                        wanted_piece_type = None     
                    break
                
                
                if selected_piece is None:
                    selected_piece = chess_board.board[row][col]
                    selected_position = (row, col)         
                elif selected_piece.color == chess_board.playing_color:
                    # up to one move and one attack, whichever is first
                    if selected_position not in moved and selected_piece != None:
                        if chess_board.move(selected_position[0], selected_position[1], row, col):
                            moved.append((row, col))
                            if selected_position in attacked:
                                attacked.remove(selected_position)
                                attacked.append((row, col))
                            selected_piece = None
                            selected_position = None
                            
                            
                    if selected_position not in attacked and selected_piece != None:
                        if chess_board.attack(selected_position[0], selected_position[1], row, col):
                            attacked.append(selected_position)
                            selected_piece = None
                            selected_position = None
                            
                            kings = [king for one_row in chess_board.board for king in one_row if isinstance(king, Piece.King)]
                            if len(kings) == 1:
                                running = False
                                winner = 'White Win' if kings[0].color == 0 else 'Black Win'
                                show_message(screen, winner)
                                
                    if selected_piece != None:
                        selected_piece = None
                        selected_position = None
                        show_message(screen, 'Not Allowed')
                else:
                    selected_piece = None
                    selected_position = None
                    show_message(screen, 'Not Allowed')
        
                    
        screen.fill((255, 255, 255))
        chess_board.draw(pieces, screen, font)
        
        done_button_text = font.render("Round Black", True, (255, 255, 255)) if chess_board.playing_color else font.render("Round White", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 139, 139), intro_button_rect)
        screen.blit(intro_button_text, (intro_button_rect.x + 40, intro_button_rect.y + 20))
        pygame.draw.rect(screen, (189, 183, 107), done_button_rect)
        screen.blit(done_button_text, (done_button_rect.x + 20, done_button_rect.y + 20))
        
        player_tokens = f"White:\n ${chess_board.tokens[0]}\n Black:\n ${chess_board.tokens[1]}"
        y_offset = 0
        for line in player_tokens.split("\n"):
            text_surface = font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (410, 650 + y_offset))
            y_offset += 30
         
        screen.blit(pieces["Pawn"][0], (0, 680))
        screen.blit(pawn_text, (pawn_rect.x + 20, pawn_rect.y + 120))
        screen.blit(pieces["Rook"][0], (80, 680))
        screen.blit(rook_text, (rook_rect.x + 20, rook_rect.y + 120))
        screen.blit(pieces["Knight"][0], (160, 680))
        screen.blit(knight_text, (knight_rect.x + 20, knight_rect.y + 120))
        screen.blit(pieces["Bishop"][0], (240, 680))
        screen.blit(bishop_text, (bishop_rect.x + 20, bishop_rect.y + 120))
        screen.blit(pieces["Queen"][0], (320, 680))
        screen.blit(queen_text, (queen_rect.x + 20, queen_rect.y + 120))
                        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())