import pygame
import random
import sys
import heapq
import time

# ----------------------------------
# CONFIG
# ----------------------------------
BOARD_SIZE = 3
TILE_SIZE = 120
MARGIN = 10
SCREEN_WIDTH = TILE_SIZE * BOARD_SIZE + 220
SCREEN_HEIGHT = TILE_SIZE * BOARD_SIZE + 60
BG_COLOR = (25, 28, 35)
TILE_COLOR = (70, 150, 255)
TILE_HIGHLIGHT = (130, 190, 255)
EMPTY_COLOR = (45, 50, 60)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 80, 120)
BUTTON_HOVER = (90, 130, 190)
PANEL_COLOR = (35, 40, 55)
DIALOG_COLOR = (40, 45, 65)
FONT_SIZE = 48
FPS = 60

# ----------------------------------
# INIT
# ----------------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("8-Puzzle (Click + Auto Solve + Dialog)")
font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

# ----------------------------------
# HELPERS
# ----------------------------------
def is_solvable(seq):
    arr = [n for n in seq if n != 0]
    inv = sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j])
    return inv % 2 == 0

def create_board():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        if is_solvable(nums) and nums != list(range(9)):
            return nums

def get_neighbors(empty_index):
    row, col = divmod(empty_index, BOARD_SIZE)
    moves = []
    if row > 0: moves.append(empty_index - BOARD_SIZE)
    if row < BOARD_SIZE - 1: moves.append(empty_index + BOARD_SIZE)
    if col > 0: moves.append(empty_index - 1)
    if col < BOARD_SIZE - 1: moves.append(empty_index + 1)
    return moves

def is_solved(board):
    return board == list(range(1, 9)) + [0]

def manhattan(state):
    dist = 0
    for idx, val in enumerate(state):
        if val == 0: continue
        goal_r, goal_c = divmod(val - 1, 3)
        r, c = divmod(idx, 3)
        dist += abs(r - goal_r) + abs(c - goal_c)
    return dist

def a_star(start):
    goal = tuple(range(1, 9)) + (0,)
    start = tuple(start)
    open_heap = []
    heapq.heappush(open_heap, (manhattan(start), 0, start))
    came = {}
    g = {start: 0}
    while open_heap:
        _, cost, cur = heapq.heappop(open_heap)
        if cur == goal:
            path = []
            while cur in came:
                cur, move = came[cur]
                path.append(move)
            path.reverse()
            return path
        empty = cur.index(0)
        for n in get_neighbors(empty):
            new_state = list(cur)
            new_state[empty], new_state[n] = new_state[n], new_state[empty]
            new_state = tuple(new_state)
            temp_g = g[cur] + 1
            if new_state not in g or temp_g < g[new_state]:
                g[new_state] = temp_g
                came[new_state] = (cur, new_state)
                f = temp_g + manhattan(new_state)
                heapq.heappush(open_heap, (f, temp_g, new_state))
    return []

# ----------------------------------
# DRAWING
# ----------------------------------
def draw_tile(x, y, val, hover=False):
    rect = pygame.Rect(x, y, TILE_SIZE - MARGIN, TILE_SIZE - MARGIN)
    color = TILE_HIGHLIGHT if hover else TILE_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=15)
    text = font.render(str(val), True, TEXT_COLOR)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def draw_board(board, hover_idx=None):
    for i, val in enumerate(board):
        row, col = divmod(i, BOARD_SIZE)
        x = col * TILE_SIZE + MARGIN
        y = row * TILE_SIZE + MARGIN
        if val == 0:
            rect = pygame.Rect(x, y, TILE_SIZE - MARGIN, TILE_SIZE - MARGIN)
            pygame.draw.rect(screen, EMPTY_COLOR, rect, border_radius=15)
        else:
            draw_tile(x, y, val, hover=(i == hover_idx))

def draw_panel(moves, elapsed, solved):
    pygame.draw.rect(screen, PANEL_COLOR, (TILE_SIZE * BOARD_SIZE + 10, 10, 200, SCREEN_HEIGHT - 20), border_radius=10)
    info_lines = [
        f"Moves: {moves}",
        f"Time: {elapsed}s",
        "",
        "[N] New Game",
        "[A] Auto Solve",
        "[U] Undo",
        "[R] Redo"
    ]
    for i, line in enumerate(info_lines):
        color = (100, 255, 100) if solved and i == 0 else TEXT_COLOR
        text = small_font.render(line, True, color)
        screen.blit(text, (TILE_SIZE * BOARD_SIZE + 30, 40 + i * 35))

def draw_dialog(moves, elapsed):
    dialog_w, dialog_h = 360, 180
    x = (SCREEN_WIDTH - dialog_w) // 2
    y = (SCREEN_HEIGHT - dialog_h) // 2
    rect = pygame.Rect(x, y, dialog_w, dialog_h)
    pygame.draw.rect(screen, DIALOG_COLOR, rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=15)
    title = font.render("Puzzle Solved!", True, (255, 230, 120))
    text1 = small_font.render(f"Moves: {moves}", True, TEXT_COLOR)
    text2 = small_font.render(f"Time: {elapsed}s", True, TEXT_COLOR)
    msg = small_font.render("Press N to start a new game", True, (180, 200, 255))
    screen.blit(title, (x + 40, y + 30))
    screen.blit(text1, (x + 120, y + 80))
    screen.blit(text2, (x + 120, y + 110))
    screen.blit(msg, (x + 40, y + 145))

# ----------------------------------
# MAIN LOOP
# ----------------------------------
def main():
    board = create_board()
    moves = 0
    undo_stack = []
    redo_stack = []
    start_time = time.time()
    solving = False
    solution = []
    solved = False
    stop_timer = False

    while True:
        elapsed = int(time.time() - start_time) if not stop_timer else elapsed
        mouse_pos = pygame.mouse.get_pos()
        hover_idx = None

        if mouse_pos[0] < TILE_SIZE * BOARD_SIZE:
            col = mouse_pos[0] // TILE_SIZE
            row = mouse_pos[1] // TILE_SIZE
            hover_idx = row * BOARD_SIZE + col

        screen.fill(BG_COLOR)
        draw_board(board, hover_idx)
        draw_panel(moves, elapsed, solved)
        if solved:
            draw_dialog(moves, elapsed)
        pygame.display.flip()

        if solving:
            if solution:
                board = list(solution.pop(0))
                moves += 1
                pygame.time.wait(30)
                if not solution:
                    solving = False
                    solved = True
                    stop_timer = True
            else:
                solving = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not solved and not solving:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    idx = hover_idx
                    if idx is not None:
                        empty = board.index(0)
                        if idx in get_neighbors(empty):
                            undo_stack.append(board.copy())
                            redo_stack.clear()
                            board[empty], board[idx] = board[idx], board[empty]
                            moves += 1
                            if is_solved(board):
                                solved = True
                                stop_timer = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    board = create_board()
                    moves = 0
                    undo_stack.clear()
                    redo_stack.clear()
                    start_time = time.time()
                    solved = False
                    stop_timer = False

                elif event.key == pygame.K_a and not solving and not solved:
                    print("Running fast A* auto-solver...")
                    solving = True
                    solution = [list(s) for s in a_star(board)]

                elif event.key == pygame.K_u and undo_stack and not solved:
                    redo_stack.append(board.copy())
                    board = undo_stack.pop()
                    moves += 1

                elif event.key == pygame.K_r and redo_stack and not solved:
                    undo_stack.append(board.copy())
                    board = redo_stack.pop()
                    moves += 1

        clock.tick(FPS)

if __name__ == "__main__":
    main()
