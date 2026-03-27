import asyncio
from itertools import cycle

from .curses_tools import draw_frame, get_frame_size, read_controls


async def draw_spaceship(canvas, coords, frame1, frame2):
    """Анимация космического корабля.

    Циклически переключает два кадра (frame1 и frame2).
    Предыдущий кадр стирается перед отрисовкой нового.
    Координаты корабля могут меняться внешним кодом (через coords).

    Args:
        canvas: curses window объект.
        coords (list): список из двух элементов [row, column] — текущие
            координаты левого верхнего угла корабля. Список изменяем,
            чтобы анимация следовала за перемещением.
        frame1 (str): первый кадр анимации (многострочная строка).
        frame2 (str): второй кадр анимации.

    Returns:
        None. Корутина работает бесконечно.
    """

    frames = cycle([frame1, frame2])
    current_frame = None
    prev_row, prev_column = coords[0], coords[1]

    while True:
        next_frame = next(frames)

        if current_frame is not None:
            draw_frame(canvas, prev_row, prev_column, current_frame, negative=True)

        draw_frame(canvas, coords[0], coords[1], next_frame)
        current_frame = next_frame
        prev_row, prev_column = coords[0], coords[1]
        canvas.refresh()

        for _ in range(2):
            await asyncio.sleep(0)


async def handle_spaceship(canvas, frame1, frame2, speed=1, exit_flag=None):
    """Управление кораблём и его анимация.

    Args:
        canvas: curses window.
        frame1, frame2: кадры анимации.
        speed: скорость перемещения (пикселей за нажатие).
    """
    frame_height, frame_width = get_frame_size(frame1)

    height, width = canvas.getmaxyx()
    ship_row = (height - frame_height) // 2
    ship_col = (width - frame_width) // 2

    frames = cycle([frame1, frame2])
    current_frame = None
    prev_row, prev_col = ship_row, ship_col

    while True:
        rows_dir, cols_dir, _, quit_pressed = read_controls(canvas)
        if quit_pressed:
            if exit_flag is not None:
                exit_flag[0] = True
            break

        ship_row += rows_dir * speed
        ship_col += cols_dir * speed

        max_row = canvas.getmaxyx()[0] - frame_height - 1
        max_col = canvas.getmaxyx()[1] - frame_width - 1
        ship_row = max(1, min(ship_row, max_row))
        ship_col = max(1, min(ship_col, max_col))

        next_frame = next(frames)

        if current_frame is not None:
            draw_frame(canvas, prev_row, prev_col, current_frame, negative=True)

        draw_frame(canvas, ship_row, ship_col, next_frame)
        current_frame = next_frame
        prev_row, prev_col = ship_row, ship_col
        canvas.refresh()

        for _ in range(2):
            await asyncio.sleep(0)
