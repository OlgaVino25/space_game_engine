import asyncio
from itertools import cycle

from .curses_tools import draw_frame


async def draw_spaceship(canvas, coords, frame1, frame2):
    """Анимация космического корабля.

    Циклически переключает два кадра (frame1 и frame2).
    Предыдущий кадр стирается перед отрисовкой нового.
    Координаты корабля могут меняться внешним кодом (через coords).

    Args:
        canvas: curses window объект.
        coords (list): список из двух элементов [row, column] — текущие
            координаты левого верхнего угла корабля. Список изменяем,
            чтобы анимация следовала за перемещением.
        frame1 (str): первый кадр анимации (многострочная строка).
        frame2 (str): второй кадр анимации.

    Returns:
        None. Корутина работает бесконечно.
    """

    frames = cycle([frame1, frame2])
    current_frame = None
    prev_row, prev_column = coords[0], coords[1]

    while True:
        next_frame = next(frames)

        if current_frame is not None:
            draw_frame(canvas, prev_row, prev_column, current_frame, negative=True)

        draw_frame(canvas, coords[0], coords[1], next_frame)
        current_frame = next_frame
        prev_row, prev_column = coords[0], coords[1]
        canvas.refresh()

        for _ in range(2):
            await asyncio.sleep(0)
