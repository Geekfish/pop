import sys
import random
import pygame

from pygame.locals import *

from colours import colours


class Corn(object):
    x = 0
    y = 0
    is_new = True
    popped = False
    speed = 0

    def __init__(self, x, speed):
        super(Corn, self).__init__()
        self.x = x
        self.speed = speed


class Pop(object):
    fps = 30
    win_width = 640
    win_height = 480
    cell_size = 20
    cell_width = win_width / cell_size
    cell_height = win_height / cell_size

    time = 0
    mouse = 0, 0
    corns = []
    time_to_next_corn = 1000
    time_since_last_corn = 0
    min_next_corn = 500
    max_next_corn = 4000

    def validate_settings(self):
        assert self.win_width % self.cell_size == 0, ("Window width must be a "
                                                      "multiple of cell size.")
        assert self.win_height % self.cell_size == 0, ("Window height must be"
                                                       "a multiple of"
                                                       "cell size.")

    def __init__(self):
        super(Pop, self).__init__()
        pygame.init()

        self.validate_settings()
        self.fps_clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(self.win_dimensions)
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Pop Pop Pop!')

    def create_corn(self):
        self.time_since_last_corn = 0
        self.time_to_next_corn = random.randint(self.min_next_corn,
                                                self.max_next_corn)
        new_corn = Corn(
            x=random.randint(1, self.cell_width - 1) * self.cell_size,
            speed=random.randint(2, 5)
        )
        self.corns.append(new_corn)

    @property
    def win_dimensions(self):
        return self.win_width, self.win_height

    def draw_grid(self):
        for x in range(0, self.win_width, self.cell_size):
            pygame.draw.line(self.display, colours.dark_grey, (x, 0),
                             (x, self.win_height))
        for y in range(0, self.win_height, self.cell_size):
            pygame.draw.line(self.display, colours.dark_grey, (0, y),
                             (self.win_width, y))

    def draw_corn(self, corn):
        if corn.popped:
            outer_rect = pygame.Rect(corn.x, corn.y,
                                     self.cell_size, self.cell_size)
            pygame.draw.rect(self.display, colours.light_grey, outer_rect)
            inner_rect = pygame.Rect(
                corn.x + 4, corn.y + 4, self.cell_size - 8, self.cell_size - 8)
            pygame.draw.rect(self.display, colours.white, inner_rect)
        else:
            half_cell = int(self.cell_size * 0.5)
            pygame.draw.circle(self.display, colours.yellow,
                               (corn.x + half_cell, corn.y + half_cell),
                               half_cell - 4)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def update_timers(self):
        self.time_since_last_corn += self.time

    def should_create_corn(self):
        return self.time_since_last_corn > self.time_to_next_corn

    def move_corns(self):
        for corn in self.corns:
            if not corn.is_new:
                corn.y += corn.speed
            else:
                corn.is_new = False
            self.draw_corn(corn)

    def draw_background(self):
        self.display.fill(colours.black)
        self.draw_grid()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEMOTION:
                    self.mouse = event.pos
                elif event.type == MOUSEBUTTONUP:
                    for corn in self.corns:
                        collision = all((
                            self.mouse[0] > corn.x,
                            self.mouse[0] < (corn.x + self.cell_width),
                            self.mouse[1] > corn.y,
                            self.mouse[1] < (corn.y + self.cell_width)))
                        if collision:
                            corn.popped = True

            self.update_timers()

            self.draw_background()

            if self.should_create_corn():
                self.create_corn()

            self.move_corns()

            pygame.display.update()
            self.time = self.fps_clock.tick(self.fps)


if __name__ == '__main__':
    game = Pop()
    game.run()
