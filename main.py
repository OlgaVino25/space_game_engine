import time
import curses
import random

from animate.blink import blink
from animate.fire import fire
from animate.spaceship import handle_spaceship


TIC_TIMEOUT = 0.1
SYMBOLS = "+*.:"
SPACESHIP_SPEED = 5

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

    coroutines = []

    for _ in range(100):
        row = random.randint(1, max_row)
        column = random.randint(1, max_column)
        symbol = random.choice(SYMBOLS)
        coroutines.append(blink(canvas, row, column, symbol))

    coroutines.append(
        fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0)
    )

    exit_flag = [False]

    coroutines.append(
        handle_spaceship(
            canvas, text_1, text_2, speed=SPACESHIP_SPEED, exit_flag=exit_flag
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

    time.sleep(2)


def main():
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
