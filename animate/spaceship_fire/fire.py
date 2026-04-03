import curses
from ..game.utils import sleep
from ..game.obstacles import obstacles_in_last_collisions


BORDER_WIDTH = 1
SHOT_SPEED = -0.3


async def fire(
    canvas,
    start_row,
    start_column,
    rows_speed=SHOT_SPEED,
    columns_speed=0,
    obstacles=None,
):
    """Анимация выстрела.

    Выстрел начинается с заданной позиции и движется с указанной скоростью.
    Сначала отображается символ "*", затем "O", после чего снаряд стирается.
    Дальше движется символом "|" (вертикально) или "-" (горизонтально)
    до достижения границы экрана. При попадании в препятствие выстрел исчезает
    и препятствие помечается для взрыва.

    Args:
        canvas: curses window объект.
        start_row (int): начальная строка выстрела.
        start_column (int): начальная колонка выстрела.
        rows_speed (float): скорость по вертикали.
        columns_speed (float): скорость по горизонтали.
        obstacles (list, optional): список препятствий.
    """
    if obstacles is None:
        obstacles = []

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await sleep(1)

    canvas.addstr(round(row), round(column), "O")
    await sleep(1)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"
    rows, cols = canvas.getmaxyx()
    max_row, max_col = rows - BORDER_WIDTH, cols - BORDER_WIDTH

    curses.beep()

    while 0 < row < max_row and 0 < column < max_col:
        r_cur, c_cur = round(row), round(column)

        for obs in obstacles:
            if obs.has_collision(r_cur, c_cur):
                if obs not in obstacles_in_last_collisions:
                    obstacles_in_last_collisions.append(obs)
                canvas.addstr(r_cur, c_cur, " ")
                return

        canvas.addstr(round(row), round(column), symbol)
        await sleep(1)
        canvas.addstr(round(row), round(column), " ")

        row += rows_speed
        column += columns_speed
