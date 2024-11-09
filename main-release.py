import pygame
import tkinter as tk
from tkinter import ttk
import chess
import chess.engine
import random

SCREEN_WIDTH = SCREEN_HEIGHT = 512
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)
SELECTED_SQUARE_COLOR = (255, 255, 0)

def load_piece_images():
    piece_images = {}
    pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
    imgs = {
        'r': 'b_rook', 'n': 'b_knight', 'b': 'b_bishop', 'q': 'b_queen',
        'k': 'b_king', 'p': 'b_pawn', 'R': 'w_rook', 'N': 'w_knight',
        'B': 'w_bishop', 'Q': 'w_queen', 'K': 'w_king', 'P': 'w_pawn',
    }
    for piece in pieces:
        img_path = f"assets/imgs/{imgs[piece]}.png"
        piece_images[piece] = pygame.image.load(img_path)
        piece_images[piece] = pygame.transform.smoothscale(piece_images[piece], (SQUARE_SIZE, SQUARE_SIZE))
    return piece_images

PIECE_IMAGES = load_piece_images()

class Sound:
    def __init__(self):
        self.check_sound = pygame.mixer.Sound("./assets/sounds/check_sound.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/sounds/start_sound.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move_sound.mp3")
        self.stalemate_sound = pygame.mixer.Sound("./assets/sounds/stalemate_sound.mp3")

import pygame
import tkinter as tk
from tkinter import ttk
import chess
import chess.engine
import random

SCREEN_WIDTH = SCREEN_HEIGHT = 512
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)
SELECTED_SQUARE_COLOR = (255, 255, 0)

def load_piece_images():
    piece_images = {}
    pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
    imgs = {
        'r': 'b_rook', 'n': 'b_knight', 'b': 'b_bishop', 'q': 'b_queen',
        'k': 'b_king', 'p': 'b_pawn', 'R': 'w_rook', 'N': 'w_knight',
        'B': 'w_bishop', 'Q': 'w_queen', 'K': 'w_king', 'P': 'w_pawn',
    }
    for piece in pieces:
        img_path = f"assets/imgs/{imgs[piece]}.png"
        piece_images[piece] = pygame.image.load(img_path)
        piece_images[piece] = pygame.transform.smoothscale(piece_images[piece], (SQUARE_SIZE, SQUARE_SIZE))
    return piece_images

PIECE_IMAGES = load_piece_images()

class Sound:
    def __init__(self):
        self.check_sound = pygame.mixer.Sound("./assets/sounds/check_sound.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/sounds/start_sound.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/sounds/move_sound.mp3")
        self.stalemate_sound = pygame.mixer.Sound("./assets/sounds/stalemate_sound.mp3")

class Game:
    def __init__(self, engine_path, player_color=chess.WHITE, skill_level=1):
        self.engine_path = engine_path
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        self.board = chess.Board()
        self.player_color = player_color
        self.selected_square = None
        self.game_over = False
        self.sound = Sound()
        self.sound.game_start_sound.play()
        self.engine.configure({"Skill Level": skill_level})
        self.scramble_board()
        self.restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 40)  

    def reset(self):
        self.sound.game_start_sound.play()
        self.board.reset()
        self.selected_square = None
        self.game_over = False
        self.scramble_board()

    def scramble_board(self):
        pieces_white = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        pieces_black = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
        random.shuffle(pieces_white)
        random.shuffle(pieces_black)
        pieces_white[pieces_white.index('K')] = 'K'
        pieces_black[pieces_black.index('k')] = 'k'
        for i in range(8):
            self.board.set_piece_at(chess.square(i, 1), chess.Piece.from_symbol(pieces_white[i + 8]))
            self.board.set_piece_at(chess.square(i, 0), chess.Piece.from_symbol(pieces_white[i]))
            self.board.set_piece_at(chess.square(i, 6), chess.Piece.from_symbol(pieces_black[i + 8]))
            self.board.set_piece_at(chess.square(i, 7), chess.Piece.from_symbol(pieces_black[i]))

    def handle_mouse_click(self, pos):
        if self.game_over and self.restart_button_rect.collidepoint(pos):  
            self.reset()
            return
        if not self.game_over and self.board.turn == self.player_color:
            row, col = self.get_square_from_mouse(pos)
            square = chess.square(col, 7 - row)
            if self.selected_square is None:
                if self.board.piece_at(square) is not None and self.board.color_at(square) == self.player_color:
                    self.selected_square = (row, col)
            else:
                move = chess.Move(chess.square(self.selected_square[1], 7 - self.selected_square[0]), square)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.sound.move_sound.play()
                self.selected_square = None

    def get_square_from_mouse(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return row, col

    def make_ai_move(self):
        if not self.game_over and self.board.turn != self.player_color:
            try:
                result = self.engine.play(self.board, chess.engine.Limit(time=1))
                self.board.push(result.move)
                self.sound.move_sound.play()
            except chess.IllegalMoveError:
                print("Illegal move generated:", result.move)

    def update_game_state(self):
        if self.board.is_checkmate() or self.board.is_stalemate():
            self.game_over = True

    def draw(self, screen):
        self.draw_board(screen)
        if self.selected_square:
            self.highlight_moves(screen)
        if self.game_over:
            self.draw_game_over(screen)

    def draw_board(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.selected_square is not None and (row, col) == self.selected_square:
                    pygame.draw.rect(screen, SELECTED_SQUARE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
                piece = str(self.board.piece_at(chess.square(col, 7 - row)))
                if piece != 'None':
                    image = PIECE_IMAGES[piece]
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def highlight_moves(self, screen):
        if self.selected_square:
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                col, row = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
                pygame.draw.circle(screen, (0, 255, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)

    def get_possible_moves(self):
        if self.selected_square:
            row, col = self.selected_square
            square = chess.square(col, 7 - row)
            piece = self.board.piece_at(square)
            if piece is not None:
                legal_moves = self.board.legal_moves
                return [move for move in legal_moves if move.from_square == square]
        return []

    def draw_game_over(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((200, 200, 200, 128))
        screen.blit(overlay, (0, 0))
        font = pygame.font.Font(None, 36)
        if self.board.is_checkmate():
            text = f"Checkmate! {'White' if self.board.turn == chess.BLACK else 'Black'} wins!"
        elif self.board.is_stalemate():
            text = "Stalemate!"
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(text_surf, text_rect)
        button_font = pygame.font.Font(None, 30)
        button_text = "Restart"
        button_surf = button_font.render(button_text, True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), self.restart_button_rect)  
        button_text_rect = button_surf.get_rect(center=self.restart_button_rect.center)
        screen.blit(button_surf, button_text_rect)

        if self.restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 0, 0), self.restart_button_rect, 3)

    def set_skill_level(self, skill_level):
        self.engine.configure({"Skill Level": skill_level})
        print(f"Difficulty set to: {skill_level}. This is just a confirmation.")  

def create_difficulty_window(game):
    def on_difficulty_select():
        skill_level = difficulty_slider.get()
        print(f"Setting difficulty to: {skill_level}") 
        game.set_skill_level(skill_level)
        difficulty_window.destroy()
        start_game()

    def start_game():
        global screen  
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("God Awful Chess")
        clock = pygame.time.Clock()
        game_loop(clock)

    def game_loop(clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    root.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.handle_mouse_click(event.pos)

            game.make_ai_move()
            game.update_game_state()
            screen.fill(WHITE)
            game.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    difficulty_window = tk.Toplevel()
    difficulty_window.title("Select difficulty")
    difficulty_label = tk.Label(difficulty_window, text="Select difficulty you want to play against Stockfish:")
    difficulty_label.pack(pady=10)

    difficulty_slider = tk.Scale(difficulty_window, from_=1, to_=20, orient="horizontal")
    difficulty_slider.set(1)  
    difficulty_slider.pack(pady=20)

    confirm_button = tk.Button(difficulty_window, text="Start!", command=on_difficulty_select, width=7, height=2)
    confirm_button.pack(pady=10)

    difficulty_window.protocol("WM_DELETE_WINDOW", lambda: on_difficulty_select())  
    difficulty_window.geometry("300x200")

    difficulty_window.mainloop()

if __name__ == "__main__":
    pygame.init()
    root = tk.Tk()
    root.withdraw()  

    game = Game(engine_path="./stockfish.exe")

    create_difficulty_window(game)