import enum
import pygame
from typing import Tuple

BLOCK_SHAPE_LEN = 4

BLOCK_START_J = -2

SDF          = 40
DAS          = 70
ARR          = 1
BASE_GRAVITY = 200

class BlockType(enum.IntEnum):
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7

BLOCK_TYPE_TO_COLOR = {
    BlockType.I: "deepskyblue1",
    BlockType.O: "gold",
    BlockType.T: "darkmagenta",
    BlockType.S: "green3",
    BlockType.Z: "crimson",
    BlockType.J: "darkslateblue",
    BlockType.L: "sienna1",
}

SHAPES = {
    BlockType.O: [
        [
            0, 0, 0, 0,    
            0, 1, 1, 0,    
            0, 1, 1, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            0, 1, 1, 0,    
            0, 1, 1, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            0, 1, 1, 0,    
            0, 1, 1, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            0, 1, 1, 0,    
            0, 1, 1, 0,    
            0, 0, 0, 0,    
        ]
    ],

    BlockType.I: [
        [
            0, 0, 0, 0,    
            1, 1, 1, 1,    
            0, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 1, 0,    
            0, 0, 1, 0,    
            0, 0, 1, 0,    
            0, 0, 1, 0,    
        ],
        [
            0, 0, 0, 0,    
            0, 0, 0, 0,    
            1, 1, 1, 1,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 1, 0, 0,    
        ],
    ],

    BlockType.T: [
        [
            0, 1, 0, 0,    
            1, 1, 1, 0,    
            0, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,    
            0, 1, 1, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            1, 1, 1, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,    
            1, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
    ],

    BlockType.S: [
        [
            0, 1, 1, 0,    
            1, 1, 0, 0,    
            0, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,    
            0, 1, 1, 0,    
            0, 0, 1, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            0, 1, 1, 0,    
            1, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            1, 0, 0, 0,    
            1, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
    ],

    BlockType.Z: [
        [
            1, 1, 0, 0,    
            0, 1, 1, 0,
            0, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 1, 0,    
            0, 1, 1, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            1, 1, 0, 0,    
            0, 1, 1, 0,
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,   
            1, 1, 0, 0,   
            1, 0, 0, 0,   
            0, 0, 0, 0,   
        ],
    ],

    BlockType.J: [
        [
            1, 0, 0, 0,    
            1, 1, 1, 0,    
            0, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 1, 0,    
            0, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            1, 1, 1, 0,    
            0, 0, 1, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,    
            0, 1, 0, 0,    
            1, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
    ],

    BlockType.L: [
        [
            0, 0, 1, 0,    
            1, 1, 1, 0,    
            0, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 1, 1, 0,    
            0, 0, 0, 0,    
        ],
        [
            0, 0, 0, 0,    
            1, 1, 1, 0,    
            1, 0, 0, 0,    
            0, 0, 0, 0,    
        ],
        [
            1, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 1, 0, 0,    
            0, 0, 0, 0,    
        ],
    ]
}

class Block:
    def __init__(self, type_, w, h, start_x, start_y):
        self.i = 2
        self.j = BLOCK_START_J
        self.w = w
        self.h = h

        self.type = type_
        self.color = BLOCK_TYPE_TO_COLOR[self.type]
        self.shapes = SHAPES[self.type]
        self.rotation = 1

        self.y_timer = 0

        self.start_x = start_x
        self.start_y = start_y

        self.right = False
        self.right_timer = 0

        self.left = False
        self.left_timer = 0

        self.rotating = False

        self.repeat_timer = 0


    def x(self):
        return self.start_x + self.i * self.w

    def y(self):
        return self.start_y + self.j * self.h

    def update(self, keys, delta):
        next_i   = self.i
        next_j   = self.j
        next_rot = self.rotation
        gravity  = BASE_GRAVITY

        if keys[pygame.K_RIGHT]:
            if self.right:
                if self.right_time > DAS:
                    if self.repeat_timer > ARR:
                        next_i = self.i + 1
                        self.repeat_timer = 0
                    else:
                        self.repeat_timer += delta
            else:
                self.right = True
                self.right_time = 0
                next_i = self.i + 1
            self.right_time += delta
        elif keys[pygame.K_LEFT]:
            if self.left:
                if self.left_time > DAS:
                    if self.repeat_timer > ARR:
                        next_i = self.i - 1
                        self.repeat_timer = 0
                    else:
                        self.repeat_timer += delta
            else:
                self.left = True
                self.left_time = 0
                next_i = self.i - 1
            self.left_time += delta
        else:
            self.right = False
            self.right_time = 0

            self.left = False
            self.left_time = 0

            self.repeat_timer = 0

        if keys[pygame.K_UP]:
            if not self.rotating:
                next_rot = (self.rotation + 1) % 4
                self.rotating = True
        elif keys[pygame.K_z]:
            if not self.rotating:
                next_rot = (self.rotation - 1) % 4
                self.rotating = True
        else:
            self.rotating = False

        if keys[pygame.K_DOWN]:
            gravity = gravity / SDF

        if self.y_timer >= gravity:
            self.y_timer = 0
            next_j = self.j + 1
        self.y_timer += delta

        return {
            "position": (next_i, next_j),
            "rotation": next_rot,
            "type":     self.type,
        }
