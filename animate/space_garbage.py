import random

from .curses_tools import draw_frame, get_frame_size
from .utils import sleep


BORDER_WIDTH = 1


def load_garbage_frames():
    """Загружает кадры мусора из файлов и возвращает список строк."""
    garbage_file = [
        "animate/duck.txt",
        "animate/hubble.txt",
        "animate/lamp.txt",
        "animate/trash_large.txt",
        "animate/trash_small.txt",
        "animate/trash_xl.txt",
    ]

    frames = []

    for file_path in garbage_file:
        with open(file_path, "r") as f:
            frames.append(f.read())

    return frames


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    _, frame_width = get_frame_size(garbage_frame)

    column = max(BORDER_WIDTH, min(column, columns_number - BORDER_WIDTH - frame_width))
    
    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await sleep(1)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, garbage_frame, coroutines, speed=0.5):
    """Бесконечно добавляет мусор на орбиту."""
    _, columns = canvas.getmaxyx()

    while True:
        delay_ticks = random.randint(5, 40)
        await sleep(delay_ticks)

        frame = random.choice(garbage_frame)
        _, frame_width = get_frame_size(frame)

        min_col = BORDER_WIDTH
        max_col = columns - BORDER_WIDTH - frame_width
        column = random.randint(min_col, max_col)

        coroutines.append(fly_garbage(canvas, column, frame, speed))
