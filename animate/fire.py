import asyncio
import curses


SHOT_SPEED = -0.3


async def fire(canvas, start_row, start_column, rows_speed=SHOT_SPEED, columns_speed=0):
    """Анимация выстрела.

    Выстрел начинается с заданной позиции и движется с указанной скоростью.
    Сначала отображается символ "*", затем "O", после чего снаряд стирается.
    Дальше движется символом "|" (вертикально) или "-" (горизонтально)
    до достижения границы экрана.

    Args:
        canvas: curses window объект.
        start_row (int): начальная строка выстрела.
        start_column (int): начальная колонка выстрела.
        rows_speed (float, optional): скорость изменения строки (положительная — вниз,
            отрицательная — вверх). По умолчанию -0.3.
        columns_speed (float, optional): скорость изменения колонки.
            По умолчанию 0 (вертикальный выстрел).

    Returns:
        None. Корутина завершается после выхода за границы экрана.
    """

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed
