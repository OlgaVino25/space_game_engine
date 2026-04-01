from .curses_tools import draw_frame
import asyncio
import random


BORDER_WIDTH = 1


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, garbage_frame, coroutines, speed=0.5):
    """Бесконечно добавляет мусор на орбиту."""
    _, columns = canvas.getmaxyx()
    min_col = BORDER_WIDTH
    max_col = columns - 2 * BORDER_WIDTH

    while True:
        delay_ticks = random.randint(20, 50)
        for _ in range(delay_ticks):
            await asyncio.sleep(0)

        frame = random.choice(garbage_frame)
        column = random.randint(min_col, max_col)

        coroutines.append(fly_garbage(canvas, column, frame, speed))
