import math
import pygame
import random
from block import BlockType, Block, SHAPES, BLOCK_TYPE_TO_COLOR, BLOCK_START_J, BLOCK_SHAPE_LEN

FPS = 60
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 1280

BACKGROUND_COLOR = (0, 0, 0)

BOARD_INVALID_ROWS = 2
BOARD_ROWS         = 20 + BOARD_INVALID_ROWS
BOARD_COLS         = 10
BOARD_CELLSIZE     = SCREEN_HEIGHT / BOARD_ROWS
BOARD_BG_CLR       = (0, 0, 0)
BOARD_STROKE_CLR   = (100, 100, 100)
BOARD_STROKE_WIDTH = 1
BOARD_START_X      = (SCREEN_WIDTH - BOARD_COLS * BOARD_CELLSIZE) / 2
BOARD_START_Y      = 0

SIDE_SIZE     = math.floor((BOARD_COLS * BOARD_CELLSIZE) / 3)
SIDE_START_X  = (BOARD_START_X - SIDE_SIZE) / 2
SIDE_PADDING  = SIDE_SIZE / 8
SIDE_CELLSIZE = ( SIDE_SIZE - SIDE_PADDING * 2 ) / BLOCK_SHAPE_LEN

class Game:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.reset()
        self.screen = None
        self.clock = None

        # for i in range(BOARD_COLS):
        #     self.board[BOARD_ROWS - 4][i] = BlockType.I
        #     self.board[BOARD_ROWS - 3][i] = BlockType.I
        #     self.board[BOARD_ROWS - 2][i] = BlockType.I
        #     self.board[BOARD_ROWS - 1][i] = BlockType.I

    def new_block(self, type_):
        return Block(
            type_   = type_,
            w       = BOARD_CELLSIZE,
            h       = BOARD_CELLSIZE,
            start_x = BOARD_START_X,
            start_y = BOARD_START_Y,
        )

    def random_block_type(self):
        return random.choice(list(BlockType))

    def random_block(self):
        type_ = self.random_block_type()
        return new_block(type_)

    def board_at(self, i, j):
        if j < 0 or j >= BOARD_ROWS or i < 0 or i >= BOARD_COLS:
            return None
        return self.board[j][i]

    def reset(self):
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.hold_block = None
        self.block_queue = [random.choice(list(BlockType)) for _ in range(5)]
        self.cur_block = self.next_block()
        self.can_hold = True

    def next_block(self):
        next_type = self.block_queue.pop(0)
        next = self.new_block(next_type)
        self.block_queue.append(self.random_block_type())
        return next

    def swap_hold(self):
        shape = self.cur_block.shapes[self.cur_block.rotation]
        self.remove_shape(shape, self.cur_block.i, self.cur_block.j)

        next = self.new_block(self.hold_block if self.hold_block else self.random_block_type())
        self.hold_block = self.cur_block.type
        self.cur_block = next

    def update(self, keys, delta):
        result = self.cur_block.update(keys, delta)

        next_rot = result["rotation"]
        next_i = result["position"][0]
        next_j = result["position"][1]
        next_shape = self.cur_block.shapes[next_rot]

        prev_rot = self.cur_block.rotation
        prev_i = self.cur_block.i
        prev_j = self.cur_block.j
        prev_shape = self.cur_block.shapes[prev_rot]

        self.remove_shape(prev_shape, prev_i, prev_j)
        can_move = True
        for dj in range(BLOCK_SHAPE_LEN):
            for di in range(BLOCK_SHAPE_LEN):
                idx = dj * BLOCK_SHAPE_LEN + di
                if not next_shape[idx]:
                    continue

                if self.cur_block.j + dj >= BOARD_ROWS:
                    can_move = False
                    break 

                try_i = next_i + di
                if try_i >= BOARD_COLS or try_i < 0:
                    can_move = False
                    break

                if self.board_at(try_i, self.cur_block.j + dj):
                    can_move = False
                    break

        if can_move:
            self.apply_shape(next_shape, next_i, prev_j, self.cur_block.type)
            self.cur_block.i = next_i
            self.cur_block.rotation = next_rot
        else:
            self.apply_shape(prev_shape, prev_i, prev_j, self.cur_block.type)

        next_shape = self.cur_block.shapes[self.cur_block.rotation]

        if next_j == self.cur_block.j:
            return False

        self.remove_shape(next_shape, self.cur_block.i, prev_j)
        for dj in range(BLOCK_SHAPE_LEN):
            for di in range(BLOCK_SHAPE_LEN):
                if self.cur_block.i + di < 0:
                    continue

                if self.cur_block.i + di >= BOARD_COLS:
                    break

                idx = dj * BLOCK_SHAPE_LEN + di
                if not next_shape[idx]:
                    continue

                try_j = next_j + dj
                # NOTE: try_j < 0?????
                if try_j >= BOARD_ROWS or self.board_at(self.cur_block.i + di, try_j):
                    self.apply_shape(next_shape, self.cur_block.i, prev_j, self.cur_block.type)
                    self.check_rows()
                    self.cur_block = self.next_block()
                    return True
        
        self.apply_shape(next_shape, self.cur_block.i, next_j, self.cur_block.type)
        self.cur_block.j = next_j
        return False

    def apply_shape(self, shape, i, j, val):
        for dj in range(BLOCK_SHAPE_LEN):
            if j + dj < 0:
                continue

            if j + dj >= BOARD_ROWS:
                return
            for di in range(BLOCK_SHAPE_LEN):
                if i + di < 0:
                    continue

                if i + di >= BOARD_COLS:
                    break
                idx = dj * BLOCK_SHAPE_LEN + di
                if shape[idx]:
                    self.board[j + dj][i + di] = val

    def remove_shape(self, shape, i, j):
        self.apply_shape(shape, i, j, None)

    def draw(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                typ = self.board[row][col]
                if not typ:
                    continue
                cell = self.cell(col, row)
                pygame.draw.rect(self.screen, BLOCK_TYPE_TO_COLOR[typ], cell)

    def side(self):
        start_x = SIDE_START_X
        start_y = BOARD_START_Y + BOARD_INVALID_ROWS * BOARD_CELLSIZE
        square = pygame.Rect(start_x, start_y, SIDE_SIZE, SIDE_SIZE)
        pygame.draw.rect(self.screen, BOARD_STROKE_CLR, square, BOARD_STROKE_WIDTH * 2)

        if self.hold_block:
            shape = SHAPES[self.hold_block][0]
            color = BLOCK_TYPE_TO_COLOR[self.hold_block]
            self.side_square(shape, color, start_x, start_y)

        start_y += SIDE_PADDING + SIDE_SIZE

        for block in self.block_queue:
            square = pygame.Rect(start_x, start_y, SIDE_SIZE, SIDE_SIZE)
            pygame.draw.rect(self.screen, BOARD_STROKE_CLR, square, BOARD_STROKE_WIDTH * 2)
            shape = SHAPES[block][0]
            color = BLOCK_TYPE_TO_COLOR[block]
            self.side_square(shape, color, start_x, start_y)
            start_y += SIDE_SIZE


    
    def side_square(self, shape, color, start_x, start_y):
        for j in range(BLOCK_SHAPE_LEN):
            for i in range(BLOCK_SHAPE_LEN):
                if shape[j * BLOCK_SHAPE_LEN + i]:
                    x = start_x + SIDE_PADDING + SIDE_CELLSIZE * i
                    y = start_y + SIDE_PADDING + SIDE_CELLSIZE * j
                    r = pygame.Rect(x, y, SIDE_CELLSIZE, SIDE_CELLSIZE)
                    pygame.draw.rect(self.screen, color, r)


    def grid(self):
        for row in self.valid_rows():
            for col in range(BOARD_COLS):
                cell = self.cell(col, row)
                pygame.draw.rect(self.screen, BOARD_STROKE_CLR, cell, BOARD_STROKE_WIDTH)
        return

    def cell(self, col, row):
        x = BOARD_START_X + col * BOARD_CELLSIZE
        y = BOARD_START_Y + row * BOARD_CELLSIZE
        cell = pygame.Rect(x, y, BOARD_CELLSIZE, BOARD_CELLSIZE)
        return cell

    def is_game_over(self):
        for row in self.invalid_rows():
            for col in range(BOARD_COLS):
                if self.board_at(col, row):
                    return True
        return False

    def invalid_rows(self):
        return range(BOARD_INVALID_ROWS)

    def valid_rows(self):
        return range(BOARD_INVALID_ROWS, BOARD_ROWS)

    def check_rows(self):
        rows_idx = BOARD_ROWS - 1
        while rows_idx >= 0:
            row = self.board[rows_idx]
            if not all(row):
                rows_idx -= 1
                continue

            self.board[rows_idx] = [None for _ in range(BOARD_COLS)]
            for other_row_idx in range(rows_idx, -1, -1):
                other_row = self.board[other_row_idx]
                for i, other in enumerate(other_row):
                    if other is not None:
                        self.board[other_row_idx + 1][i] = other
                        self.board[other_row_idx][i] = None
            
    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        clock = pygame.time.Clock()
        run = True
        delta = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                run = False

            if keys[pygame.K_r]:
                self.reset()

            if keys[pygame.K_c]:
                if self.can_hold:
                    self.can_hold = False
                    self.swap_hold()

            placed = self.update(keys, delta)
            if placed:
                if self.is_game_over():
                    self.reset()
                self.can_hold = True

            self.screen.fill(BACKGROUND_COLOR)
            self.side()
            self.grid()
            self.draw()
            pygame.display.flip()

            delta = clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
