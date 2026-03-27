import asyncio
from itertools import cycle

from .curses_tools import draw_frame, get_frame_size, read_controls


BORDER_OFFSET = 1


async def handle_spaceship(canvas, frame1, frame2, speed=1, exit_flag=None):
    """Управление кораблём и его анимация.

    Args:
        canvas: curses window.
        frame1, frame2: кадры анимации.
        speed: скорость перемещения (пикселей за нажатие).
        exit_flag: список из одного элемента [bool], при нажатии Esc
                   устанавливает exit_flag[0] = True.
    """
    frame_height, frame_width = get_frame_size(frame1)

    height, width = canvas.getmaxyx()
    ship_row = (height - frame_height) // 2
    ship_col = (width - frame_width) // 2

    frames_sequence = [frame1, frame1, frame2, frame2]
    frames = cycle(frames_sequence)
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

        max_row = canvas.getmaxyx()[0] - frame_height - BORDER_OFFSET
        max_col = canvas.getmaxyx()[1] - frame_width - BORDER_OFFSET
        ship_row = max(BORDER_OFFSET, min(ship_row, max_row))
        ship_col = max(BORDER_OFFSET, min(ship_col, max_col))

        next_frame = next(frames)

        if current_frame is not None:
            draw_frame(canvas, prev_row, prev_col, current_frame, negative=True)

        draw_frame(canvas, ship_row, ship_col, next_frame)
        current_frame = next_frame
        prev_row, prev_col = ship_row, ship_col

        await asyncio.sleep(0)
