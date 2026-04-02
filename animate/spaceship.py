from itertools import cycle

from .curses_tools import draw_frame, get_frame_size, read_controls
from .fire import fire
from .utils import sleep
from .physics import update_speed
from .obstacles import Obstacle


BORDER_OFFSET = 1


async def handle_spaceship(
    canvas,
    frame1,
    frame2,
    coroutines,
    speed_limit=2,
    fading=0.8,
    exit_flag=None,
    obstacles=None,
):
    """Управление кораблём с плавной физикой и стрельбой по пробелу.

    Args:
        canvas: curses window.
        frame1, frame2: кадры анимации.
        coroutines: список корутин для добавления выстрелов.
        speed_limit: максимальная скорость по осям.
        fading: коэффициент трения (0..1).
        exit_flag: список [bool] для сигнала выхода.
        obstacles: список препятствий для проверки столкновений.
    """

    frame_height, frame_width = get_frame_size(frame1)

    height, width = canvas.getmaxyx()
    ship_row = (height - frame_height) // 2
    ship_col = (width - frame_width) // 2

    row_speed = 0.0
    col_speed = 0.0

    frames_sequence = [frame1, frame1, frame2, frame2]
    frames = cycle(frames_sequence)
    current_frame = None
    prev_row, prev_col = ship_row, ship_col

    while True:
        rows_dir, cols_dir, space_pressed, quit_pressed = read_controls(canvas)
        if quit_pressed:
            if exit_flag is not None:
                exit_flag[0] = True
            break

        if space_pressed:
            shot_row = ship_row
            shot_col = ship_col + frame_width // 2
            coroutines.append(fire(canvas, shot_row, shot_col, obstacles=obstacles))

        row_speed, col_speed = update_speed(
            row_speed,
            col_speed,
            rows_dir,
            cols_dir,
            row_speed_limit=speed_limit,
            column_speed_limit=speed_limit,
            fading=fading,
        )

        ship_row += row_speed
        ship_col += col_speed

        max_row = canvas.getmaxyx()[0] - frame_height - BORDER_OFFSET
        max_col = canvas.getmaxyx()[1] - frame_width - BORDER_OFFSET
        ship_row = max(BORDER_OFFSET, min(ship_row, max_row))
        ship_col = max(BORDER_OFFSET, min(ship_col, max_col))

        if obstacles:
            ship_bbox = (ship_row, ship_col, frame_height, frame_width)
            for obs in obstacles:
                if obs.has_collision(ship_row, ship_col, frame_height, frame_width):
                    if exit_flag is not None:
                        exit_flag[0] = True
                    if current_frame is not None:
                        draw_frame(
                            canvas, prev_row, prev_col, current_frame, negative=True
                        )
                    return

        next_frame = next(frames)

        if current_frame is not None:
            draw_frame(canvas, prev_row, prev_col, current_frame, negative=True)

        draw_frame(canvas, ship_row, ship_col, next_frame)
        current_frame = next_frame
        prev_row, prev_col = ship_row, ship_col

        await sleep(1)
