from random import randint
import numpy as np
import pygame
import time
import sys
import os


def start_screen(screen):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    Fps = 50
    clock = pygame.time.Clock()
    fon = screen
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(Fps)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen2(screen, surfac):
    intro_text = ["ПОБЕДА", "",
                  "ПОБЕДА",
                  "ПОБЕДА",
                  "ПОБЕДА"]
    Fps = 50
    clock = pygame.time.Clock()
    fon = surfac
    # fon = screen

    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True  # начинаем игру
        pygame.display.flip()
        clock.tick(Fps)


class Board:
    # создание поля размером width на height
    def __init__(self, width, height, level):
        self.width = width  # ширшна поля
        self.height = height
        self.level = level
        self.board = [[0] * width for _ in range(height)]
        # отступы слева и сверху, размер ячейки
        self.left = 20
        self.top = 20
        self.cell_size = 30
        self.current_cell = ()
        #  self.cell_coords = ()
        self._start_field()
        self.flag_finish = False

    def _start_field(self):
        self.num_dict = {}
        # print('введите уроень перемешивания')
        # level=int(input())

        candidate_cell_coords = (np.random.randint(self.width), np.random.randint(self.height))
        # print('candidate_cell_coords', candidate_cell_coords)
        num_list = [i for i in range(1, self.width ** 2)]
        num_list.append(0)
        # print('num_list', num_list)
        for y in range(self.height):
            for x in range(self.width):
                # print('xy', x, y)
                self.num_dict[(x, y)] = num_list[self.width * y + x]
                if self.num_dict[(x, y)] == 0:
                    self.empty_cell = (x, y)
                    i = 0
        while i < self.level:
            for x in range(self.height):
                for y in range(self.width):
                    if (candidate_cell_coords[0] + 1, candidate_cell_coords[1]) == self.empty_cell or \
                            (candidate_cell_coords[0] - 1, candidate_cell_coords[1]) == self.empty_cell or \
                            (candidate_cell_coords[0], candidate_cell_coords[1] + 1) == self.empty_cell or \
                            (candidate_cell_coords[0], candidate_cell_coords[1] - 1) == self.empty_cell:
                        b = self.num_dict[candidate_cell_coords]
                        self.num_dict[candidate_cell_coords] = 0
                        self.num_dict[self.empty_cell] = b
                        self.empty_cell = candidate_cell_coords
                        i += 1
                        candidate_cell_coords = (np.random.randint(self.width), np.random.randint(self.height))
                    # print('empty cell', x, y, 'cell coords', candidate_cell_coords)  # empty cell

                    else:
                        pass  # print('not neighbouring cell, new attempt;', candidate_cell_coords)
            candidate_cell_coords = (np.random.randint(self.width), np.random.randint(self.height))
        # print('start_field', self.num_dict)

        #print(i)

    def draw_num(self):
        # print('draw_num')
        for y in range(self.height):
            for x in range(self.width):
                if self.num_dict[(x, y)] == 0:
                    continue
                font = pygame.font.Font(None, 30)
                text = font.render(str(self.num_dict[(x, y)]), False, (100, 255, 100))
                screen.blit(text, (x * self.cell_size + self.left + int(self.cell_size / 2),
                                   y * self.cell_size + self.top + int(self.cell_size / 2)))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)
        self.draw_num()
        if self.is_win():
            print('win')
            self.flag_finish = True

        # if self.current_cell:  # не пусто
        #     if (self.current_cell[0] >= 0 and self.current_cell[0] <= 3) and \
        #             (self.current_cell[1] >= 0 and self.current_cell[1] <= 3):
        #         self.on_click(self.current_cell, screen)

    def is_win(self):
        # print('enter is win')
        # print(self.num_dict)
        if self.num_dict[(0, 0)] != 1 or self.num_dict[(self.width - 1, self.height - 1)] != 0:
            return False
        else:
            i = 0
            for x in range(self.height):
                # print('x', x)

                for y in range(self.width):
                    # print('x', x, 'y', y)
                    if (x == 0 and y == 0) or (x == self.width - 1 and y == self.height - 1):
                        continue

                    else:

                        if self.num_dict[(x, y)] != self.width * y + x + 1:
                            i += 1
                            # print('2y+x+1', self.width * y + x + 1, 'i=', i)

            if self.num_dict[(self.width - 1, self.height - 1)] == 0 and i == 0:
                print('you win')
                return True

    def get_click(self, mouse_pos, screen):
        self.current_cell = self.get_cell(mouse_pos)
        self.on_click(self.current_cell, screen)

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        cell_coords = (mouse_x - self.left) // self.cell_size, \
                      (mouse_y - self.top) // self.cell_size

        return cell_coords

    def on_click(self, cell_coords, screen):
        if cell_coords[0] < 0 or cell_coords[0] > 3 or cell_coords[1] < 0 or cell_coords[1] > 3:
            return
        if (cell_coords[0] + 1, cell_coords[1]) == self.empty_cell or \
                (cell_coords[0] - 1, cell_coords[1]) == self.empty_cell or \
                (cell_coords[0], cell_coords[1] + 1) == self.empty_cell or \
                (cell_coords[0], cell_coords[1] - 1) == self.empty_cell:
            b = self.num_dict[cell_coords]
            self.num_dict[cell_coords] = 0
            self.num_dict[self.empty_cell] = b
            self.empty_cell = cell_coords

        # rect_centre = (cell_coords[0] * self.cell_size + self.left, cell_coords[1] * self.cell_size + self.top)
        #
        # # Drawing Rectangle
        # pygame.draw.rect(screen, (0, 255, 25),
        #                  pygame.Rect(rect_centre[0], rect_centre[1], self.cell_size, self.cell_size))
        # pygame.display.flip()


pygame.init()
pygame.font.init()
size = 600, 600
screen = pygame.display.set_mode(size)
surfac = pygame.Surface((size[0], size[1]))
surfac.fill((234, 0, 34))
start_screen = start_screen(screen)
level = 5
board = Board(3, 3, level)

board.set_view(50, 50, 55)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos, screen)
            pygame.display.update()
            break

    screen.fill((0, 0, 0))
    board.render(screen)  # прорисовка поля
    if board.flag_finish or board.is_win():
        start_screen = start_screen2(screen, surfac)
        level += 6
        print(level)
        board = Board(3, 3, level)
        board.set_view(50, 50, 55)
        if level > 35:
            running = False
        # time.sleep(2)
        #running = False
        continue
    pygame.display.flip()

if start_screen2:
    board = Board(4, 4, level)
    run = True
    board.set_view(50, 50, 55)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos, screen)
                pygame.display.update()
                break

        screen.fill((0, 0, 0))
        board.render(screen)  # прорисовка поля
        if board.flag_finish or board.is_win():
            start_screen = start_screen2(screen, surfac)

            continue

        pygame.display.flip()