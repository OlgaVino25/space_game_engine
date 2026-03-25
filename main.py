import time
import curses
import random

from animate.blink import blink
from animate.fire import fire
from animate.spaceship import draw_spaceship
from animate.curses_tools import get_frame_size, read_controls


TIC_TIMEOUT = 0.1
SYMBOLS = "+*.:"
SPACESHIP_SPEED = 1

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

    max_row = height - 2
    max_column = width - 2

    start_row = height // 2
    start_column = width // 2

    frame_height, frame_width = get_frame_size(text_1)
    ship_start_row = (height - frame_height) // 2
    ship_start_column = (width - frame_width) // 2
    ship_coords = [ship_start_row, ship_start_column]

    coroutines = []

    for _ in range(100):
        row = random.randint(1, max_row)
        column = random.randint(1, max_column)
        symbol = random.choice(SYMBOLS)
        coroutines.append(blink(canvas, row, column, symbol))

    coroutines.append(
        fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0)
    )

    coroutines.append(draw_spaceship(canvas, ship_coords, text_1, text_2))

    while coroutines:
        rows_dir, cols_dir, _, quit_pressed = read_controls(canvas)

        if quit_pressed:
            break

        ship_coords[0] += rows_dir * SPACESHIP_SPEED
        ship_coords[1] += cols_dir * SPACESHIP_SPEED
        ship_coords[0] = max(1, min(ship_coords[0], max_row - frame_height + 1))
        ship_coords[1] = max(1, min(ship_coords[1], max_column - frame_width + 1))

        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)

    time.sleep(2)


def main():
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
