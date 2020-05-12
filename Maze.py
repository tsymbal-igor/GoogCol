#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import random

# In[ ]:


def make_odd(v):
    if (v//2 - v/2) == 0:
        v += 1
    return v

# In[ ]:


def initMaze(hight=13, width=13):
    """
    Создаем заготовку лабиринта
    размером hight х width
    паддингом 1
    """
    hight, width = make_odd(hight), make_odd(width)

    maze = np.zeros([hight, width])
    padding = np.ones([hight-2, width-2])
    maze[1:maze.shape[0] - 1, 1:maze.shape[1] - 1] = padding
    return maze

# In[ ]:


def isMazeNotGood(maze, wall_code=1):
    """
    Проверяем качество лабиринта
    в нем не должно остаться стен 2х2

    """

    notgood_flag = False
    hight, width = maze.shape

    for x in range(0, width):
        for y in range(0, hight):
            if maze[1+y: 3+y, 1+x: 3+x].sum() == wall_code*4:
                notgood_flag = True
    return notgood_flag
# In[ ]:


def mazegen(seed, maze, print_every_iter=0, hoop_flag=False, hoop_threshold=1000):
    """
    генератор лабиринта
    # "-1" - проход
    # "0" - границы
    # "1" - поле для прорубки лабиринта
    """
    iternum = 0

    make_hoop_flag=False

    random.seed(seed)   # инициализируем случайные числа чтобы иметь
                        # возможность повторить результат

    x, y = 1, 1         # начинаем строить лабиринт из точки [1,1]
    maze[y, x] = -1

    hight, width = maze.shape

    while isMazeNotGood(maze):  # прорубаем лабиринт
                                # пока в нем остаются стены 2х2

        direct = random.randint(1, 4)   # определяем направление движения

        if direct == 1:  # вверх
            dx = 0
            dy = -1
        elif direct == 2:  # вправо
            dx = 1
            dy = 0
        elif direct == 3:  # вниз
            dx = 0
            dy = 1
        elif direct == 4:  # влево
            dx = -1
            dy = 0

        if ((x+2*dx > 0) and (x+2*dx < width - 1) and
            (y+2*dy > 0) and (y+2*dy < hight - 1)):

            # прорубаем проход если за стеной уже нет прохода
            # либо возвращаемся по уже прорубленному проходу
            is_not_single_wall_ahead = ((maze[y+dy, x+dx] == 1) &
                                        (maze[y+2*dy, x+2*dx] != -1))
            is_pass_ahead = maze[y+dy, x+dx] == -1

            if ((is_not_single_wall_ahead or (hoop_flag and make_hoop_flag)) or
                is_pass_ahead):
            #  if (((maze[y+dy, x+dx] == 1) & (maze[y+2*dy, x+2*dx] != -1)) |
            #  (maze[y+dy, x+dx] == -1)):

                # прорубаем две клетки и запоминаем текущее положение
                maze[y+dy, x+dx] = -1
                maze[y+2*dy, x+2*dx] = -1
                x += 2*dx
                y += 2*dy
        iternum += 1

        if ((print_every_iter != 0) and ((iternum//300-iternum/300) == 0)):
            print('количество итераций', iternum)

        if (iternum//hoop_threshold-iternum/hoop_threshold) == 0:
            make_hoop_flag = True
        else:
            make_hoop_flag = False

    return maze
# In[ ]:


def showmaze(maze):

    hight, width = maze.shape

    for y in range(hight):
        print('')
        for x in range(width):
            if ((maze[y, x] == 0) or (maze[y, x] == 1)):
                print('# ', end='')
            else:
                print('  ', end='')

# In[ ]:


for n in range(1):

    maze = initMaze(25, 30)
    maze = mazegen(n, maze, 300, True, hoop_threshold=200)
    showmaze(maze)

    print('\n')

