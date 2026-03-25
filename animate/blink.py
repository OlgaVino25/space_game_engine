import asyncio
import curses
import random


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
    for _ in range(start_delay):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)
