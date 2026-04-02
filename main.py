import time
import curses
import random

from animate.blink import blink
from animate.fire import fire
from animate.spaceship import handle_spaceship
from animate.obstacles import show_obstacles
from animate.space_garbage import fill_orbit_with_garbage, load_garbage_frames


BORDER_WIDTH = 1
MIN_COORD = BORDER_WIDTH + 1
TIC_TIMEOUT = 0.1
SYMBOLS = "+*.:"
STARS_COUNT = 100
SPACESHIP_SPEED = 5
EXIT_PAUSE = 2
GARBAGE_FRAMES = load_garbage_frames()

with open("animate/rocket_frame_1.txt", "r") as file_1:
    text_1 = file_1.read()

with open("animate/rocket_frame_2.txt", "r") as file_2:
    text_2 = file_2.read()


def draw(canvas):
    """Основной игровой цикл.

    Инициализирует окно, создаёт звёзды, выстрел и корабль.
    В цикле обрабатывает ввод, обновляет позицию корабля,
    продвигает все корутины и обновляет экран.

    Args:
        canvas: curses window объект, переданный curses.wrapper.

    Returns:
        None.
    """
    curses.curs_set(False)
    canvas.border("|", "|")
    canvas.nodelay(True)
    canvas.refresh()

    height, width = canvas.getmaxyx()
    max_row = height - 2 * BORDER_WIDTH
    max_column = width - 2 * BORDER_WIDTH

    start_row = height // 2
    start_column = width // 2

    obstacles = []

    coroutines = []

    for _ in range(STARS_COUNT):
        row = random.randint(MIN_COORD, max_row)
        column = random.randint(MIN_COORD, max_column)
        symbol = random.choice(SYMBOLS)
        coroutines.append(blink(canvas, row, column, symbol))

    coroutines.append(
        fire(
            canvas,
            start_row,
            start_column,
            rows_speed=-0.3,
            columns_speed=0,
            obstacles=obstacles,
        )
    )

    # coroutines.append(show_obstacles(canvas, obstacles))

    coroutines.append(
        fill_orbit_with_garbage(canvas, GARBAGE_FRAMES, coroutines, obstacles=obstacles)
    )

    exit_flag = [False]

    coroutines.append(
        handle_spaceship(
            canvas,
            text_1,
            text_2,
            coroutines,
            speed_limit=2,
            fading=0.8,
            exit_flag=exit_flag,
            obstacles=obstacles,
        )
    )

    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)

        if exit_flag[0]:
            break

    time.sleep(EXIT_PAUSE)


def main():
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
