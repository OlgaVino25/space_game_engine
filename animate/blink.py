import curses
import random

from .utils import sleep


async def blink(canvas, row, column, symbol="*"):
    """Анимация мерцающей звезды.

    Звезда циклически меняет яркость: тусклая → обычная → яркая → обычная.
    Каждая фаза длится определённое количество тиков (задано циклами for).
    Начальная фаза случайна.

    Args:
        canvas: curses window объект, на котором рисуется звезда.
        row (int): строка, в которой находится звезда.
        column (int): колонка, в которой находится звезда.
        symbol (str, optional): символ звезды. По умолчанию "*".

    Returns:
        None. Корутина работает бесконечно.
    """

    start_delay = random.randint(0, 30)
    await sleep(start_delay)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)

        canvas.addstr(row, column, symbol)
        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)
