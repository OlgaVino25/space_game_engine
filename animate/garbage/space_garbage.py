import random

from ..tools.curses_tools import draw_frame, get_frame_size
from ..game.utils import sleep
from ..game.obstacles import Obstacle, obstacles_in_last_collisions
from ..game.explosion import explode
from ..game.game_scenario import get_garbage_delay_tics


BORDER_WIDTH = 1
MIN_GARBAGE_DELAY_TICKS = 1
MAX_GARBAGE_DELAY_TICKS = 40
GARBAGE_FRAME_DELAY = 1


def load_garbage_frames():
    """Загружает кадры мусора из файлов."""

    garbage_file = [
        "animate/garbage/duck.txt",
        "animate/garbage/hubble.txt",
        "animate/garbage/lamp.txt",
        "animate/garbage/trash_large.txt",
        "animate/garbage/trash_small.txt",
        "animate/garbage/trash_xl.txt",
    ]
    frames = []
    for file_path in garbage_file:
        with open(file_path, "r") as f:
            frames.append(f.read())
    return frames


async def fly_garbage(
    canvas,
    column,
    garbage_frame,
    speed=0.5,
    obstacles=None,
    coroutines=None,
    current_year=None,
):
    """Анимация падения мусора. При попадании выстрела – взрыв.

    Args:
        canvas: curses window.
        column (int): колонка, по которой падает мусор.
        garbage_frame (str): кадр мусора.
        speed (float): скорость падения (строк за тик).
        obstacles (list): список препятствий для регистрации.
        coroutines (list): список корутин для добавления взрыва.
    """

    rows_number, columns_number = canvas.getmaxyx()
    frame_height, frame_width = get_frame_size(garbage_frame)
    column = max(BORDER_WIDTH, min(column, columns_number - BORDER_WIDTH - frame_width))
    row = 0
    obstacle = Obstacle(row, column, frame_height, frame_width)
    if obstacles is not None:
        obstacles.append(obstacle)

    try:
        while row < rows_number:
            if obstacle in obstacles_in_last_collisions:
                obstacles_in_last_collisions.remove(obstacle)
                if coroutines is not None:
                    center_row = row + frame_height / 2
                    center_col = column + frame_width / 2
                    coroutines.append(explode(canvas, center_row, center_col))
                return

            obstacle.row = row
            obstacle.column = column
            draw_frame(canvas, row, column, garbage_frame)
            await sleep(GARBAGE_FRAME_DELAY)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
    finally:
        if obstacles is not None and obstacle in obstacles:
            obstacles.remove(obstacle)


async def fill_orbit_with_garbage(
    canvas, garbage_frame, coroutines, speed=0.5, obstacles=None, current_year=None
):
    """Бесконечно добавляет мусор на орбиту, используя текущий год для задержки.

    Args:
        canvas: curses window.
        garbage_frames (list): список кадров мусора.
        coroutines (list): список корутин для добавления новых объектов.
        speed (float): скорость падения мусора.
        obstacles (list): список препятствий.
    """

    _, columns = canvas.getmaxyx()

    while True:
        if current_year is None:
            delay_ticks = random.randint(
                MIN_GARBAGE_DELAY_TICKS, MAX_GARBAGE_DELAY_TICKS
            )
        else:
            delay_ticks = get_garbage_delay_tics(current_year[0])
            if delay_ticks is None:
                await sleep(10)
                continue

        await sleep(delay_ticks)

        frame = random.choice(garbage_frame)
        _, frame_width = get_frame_size(frame)
        min_col = BORDER_WIDTH
        max_col = columns - BORDER_WIDTH - frame_width
        column = random.randint(min_col, max_col)
        coroutines.append(
            fly_garbage(
                canvas, column, frame, speed, obstacles, coroutines, current_year
            )
        )
