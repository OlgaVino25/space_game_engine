import time
import curses
import random

from animate.game.blink import blink
from animate.spaceship_fire.spaceship import handle_spaceship
from animate.garbage.space_garbage import fill_orbit_with_garbage, load_garbage_frames
from animate.game.game_over import show_gameover
from animate.game.year_updater import update_year


BORDER_WIDTH = 1
MIN_COORD = BORDER_WIDTH + 1
TIC_TIMEOUT = 0.1
YEAR_TICKS = 15
SYMBOLS = "+*.:"
STARS_COUNT = 100
EXIT_PAUSE = 2
GARBAGE_FRAMES = load_garbage_frames()

with open("animate/spaceship_fire/rocket_frame_1.txt", "r") as file_1:
    text_1 = file_1.read()

with open("animate/spaceship_fire/rocket_frame_2.txt", "r") as file_2:
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

    info_height = 3
    info_win = canvas.derwin(info_height, width - 2, height - info_height - 1, 1)
    info_win.refresh()

    max_row = height - 2 * BORDER_WIDTH
    max_column = width - 2 * BORDER_WIDTH

    current_year = [1957]

    obstacles = []

    coroutines = []

    for _ in range(STARS_COUNT):
        row = random.randint(MIN_COORD, max_row)
        column = random.randint(MIN_COORD, max_column)
        symbol = random.choice(SYMBOLS)
        coroutines.append(blink(canvas, row, column, symbol))

    coroutines.append(update_year(info_win, current_year))

    coroutines.append(
        fill_orbit_with_garbage(
            canvas,
            GARBAGE_FRAMES,
            coroutines,
            obstacles=obstacles,
            current_year=current_year,
        )
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
            current_year=current_year,
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
