import pygame, sys
pygame.init()
pygame.mixer.init()

sound = {
    "move": pygame.mixer.Sound("coin-257878.mp3"),
    "win": pygame.mixer.Sound("8-bit-video-game-win-level-sound-version-1-145827.mp3"),
    "draw": pygame.mixer.Sound("win-sound-effect-187097.mp3")
}

# Constants
WIDTH, HEIGHT = 600,700
BOARD_SIZE = 600
LINE_WIDTH = 10
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
SQUARE_SIZE2 = SQUARE_SIZE * 2
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

# Colors (R, G, B)
themes = {
    "classic": {"bg_color": (211,211,211), "line_color": (51,51,51)},
    "futuristic": {"bg_color": (58,12,163), "line_color": (76,201,240)},
    "nature": {"bg_color": (42,126,25), "line_color": (212,225,87)}
}
WHITE = (255, 255, 255)

BG_COLOR = (0,0,0)
LINE_COLOR = (0,0,0)
CIRCLE_COLOR = (0,0,0)
CROSS_COLOR = (0,0,0)
BLACK_COLOR = (0, 0, 0)


theme_name = "classic"
def theme_colors():
    global background_color, LINE_COLOR, CIRCLE_COLOR, CROSS_COLOR
    t = themes[theme_name]
    background_color = t["bg_color"]
    LINE_COLOR = t["line_color"]
    CIRCLE_COLOR = LINE_COLOR
    CROSS_COLOR = LINE_COLOR

theme_colors()

# Themes tab constants
normal_font = pygame.font.SysFont(None, 22)
big_font = pygame.font.SysFont(None, 44)
small_font = pygame.font.SysFont(None, 18)

tab_height = 28
themes_button = pygame.Rect(6, 2, 80, tab_height-4)
show_theme = False
# dropdown theme panel
theme_panel = pygame.Rect(6, tab_height+4, 160, 0)
ITEM_HEIGHT   = 26
ITEM_GAP = 4
PANEL_PAD = 4 
def theme_item_buttons():
    theme_panel.height = PANEL_PAD + len(themes) * (ITEM_HEIGHT + ITEM_GAP)
    buttons = []
    y = theme_panel.y + PANEL_PAD
    for name in themes.keys():
        r = pygame.Rect((theme_panel.x + PANEL_PAD), y, (theme_panel.width - 2 * PANEL_PAD), ITEM_HEIGHT)
        buttons.append((name, r))
        y += ITEM_HEIGHT + ITEM_GAP
    return buttons

def draw_menu_bar():
    # Themes tab button
    pygame.draw.rect(screen, (250,250,250), themes_button, border_radius=4)
    pygame.draw.rect(screen, (210,210,210), themes_button, 1, border_radius=4)
    screen.blit(normal_font.render("Themes", True, BLACK_COLOR), (themes_button.x + 8, themes_button.y + 5))
    if not show_theme:
        return
    else:
        pygame.draw.rect(screen, (250,250,250), theme_panel, border_radius=6)
        pygame.draw.rect(screen, (210,210,210), theme_panel, 1, border_radius=6)
        for name, r in theme_item_buttons():
            pygame.draw.rect(screen, (245,245,245), r, border_radius=4)
            pygame.draw.rect(screen, (220,220,220), r, 1, border_radius=4)
            marker = "• " if name == theme_name else "  "
            screen.blit(normal_font.render(marker + name.capitalize(), True, BLACK_COLOR), (r.x+6, r.y+5))




# Bottom status bar
STATUS_HEIGHT = HEIGHT - BOARD_SIZE  
STATUS_BAR = pygame.Rect(0, BOARD_SIZE, WIDTH, STATUS_HEIGHT)

x_wins = 0
o_wins = 0

def draw_status_bar():
    # white strip
    pygame.draw.rect(screen, WHITE, STATUS_BAR)

    # counters centered-ish
    turn_text = f"Turn: {player}"  # shows X or O
    scores_text = f"Player X: {x_wins}   Player O: {o_wins}"
    text = f"{turn_text}    |    {scores_text}"

    label = big_font.render(text, True, BLACK_COLOR)
    label_x = STATUS_BAR.x + (STATUS_BAR.width - label.get_width()) // 2
    label_y = STATUS_BAR.y + (STATUS_BAR.height - label.get_height()) // 2
    screen.blit(label, (label_x, label_y))
    # small restart hint bottom-right
    hint = small_font.render("(press R to restart & close the tab)", True, BLACK_COLOR)
    screen.blit(hint, (WIDTH - hint.get_width() - 16, BOARD_SIZE + STATUS_HEIGHT - hint.get_height() - 10))




screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" TIC TAC TOE ❌⭕")
screen.fill(background_color)

# Board
board = [[None, None, None], [None, None, None], [None, None, None]]

def draw_lines():
    # horizontal line
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE2), (WIDTH, SQUARE_SIZE2), LINE_WIDTH)
    # Vertical line
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE2, 0), (SQUARE_SIZE2, BOARD_SIZE), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
       for col in range(COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    return all(all(cell is not None for cell in row) for row in board)

def check_win(player):
    # Vertical
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            draw_vertical_winning_line(col, player)
            return True
    # Horizontal
    for row in range(ROWS):
        if all(board[row][col] == player for col in range(COLS)):
            draw_horizontal_winning_line(row, player)
            return True
    # Ascending Diagonal
    if all(board[row][col] == player for row, col in zip(range(ROWS), range(COLS))):
        draw_desc_diagonal(player)
        return True
    # Descending Diagonal
    if all(board[row][col] == player for row, col in zip(range(ROWS), reversed(range(COLS)))):
        draw_asc_diagonal(player)
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 10), (posX, BOARD_SIZE - 10), LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (10, posY), (WIDTH - 10, posY), LINE_WIDTH)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (10, BOARD_SIZE - 10), (WIDTH - 10, 10), LINE_WIDTH)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (10, 10), (WIDTH - 10, BOARD_SIZE - 10), LINE_WIDTH)

def restart():
    screen.fill(background_color)
    draw_menu_bar() 
    draw_lines()
    for row in range(ROWS):
        for col in range(COLS):
            board[row][col] = None

# Main loop
draw_menu_bar()
draw_lines()
player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Handle Themes tab / dropdown 
            if themes_button.collidepoint(mx, my):
                show_theme = not show_theme  
            elif show_theme and theme_panel.collidepoint(mx, my):
                for name, r in theme_item_buttons():
                    if r.collidepoint(mx, my):
                        theme_name = name
                        theme_colors()
                        restart()
                        show_theme = False 
                        break

            elif not game_over:
                # Board click
                clicked_row = my // SQUARE_SIZE
                clicked_col = mx // SQUARE_SIZE
                if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        sound["move"].play()  # play move sound

                        if check_win(player):
                            sound["win"].play()   # win sound
                            game_over = True
                            if player == 'X':
                                x_wins += 1
                            else:
                                o_wins += 1
                                draw_figures()
                                draw_status_bar()
                        else:
                            if is_board_full():
                                sound["draw"].play()  # draw sound
                                game_over = True
                            else:
                                player = 'O' if player == 'X' else 'X'
                        draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False
                player = 'X'
                screen.fill(background_color)
                draw_menu_bar()
                draw_lines()
                draw_figures()
                draw_status_bar()
                show_theme = False


    draw_menu_bar()
    draw_status_bar()
    pygame.display.update()
