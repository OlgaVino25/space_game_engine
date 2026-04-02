import time
import curses
import random

from animate.blink import blink
from animate.fire import fire
from animate.spaceship import handle_spaceship
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


def show_gameover(canvas):
    """Отображает надпись GAME OVER в центре экрана."""
    height, width = canvas.getmaxyx()
    try:
        with open("gameover_art.txt", "r") as f:
            art_lines = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        art_lines = ["GAME OVER"]

    art_height = len(art_lines)
    art_width = max(len(line) for line in art_lines) if art_lines else 0

    if art_height <= height and art_width <= width:
        start_row = (height - art_height) // 2
        start_col = (width - art_width) // 2
        for i, line in enumerate(art_lines):
            try:
                canvas.addstr(start_row + i, start_col, line)
            except curses.error:
                pass
    else:
        msg = "GAME OVER"
        x = (width - len(msg)) // 2
        y = height // 2
        canvas.addstr(y, x, msg)


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

    canvas.clear()
    canvas.border("|", "|")
    show_gameover(canvas)
    canvas.refresh()

    time.sleep(EXIT_PAUSE)


def main():
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
