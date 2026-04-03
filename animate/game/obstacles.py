import asyncio
from ..tools.curses_tools import draw_frame


obstacles_in_last_collisions = []


class Obstacle:
    """Препятствие (мусор) на игровом поле.

    Attributes:
        row (int): верхняя строка препятствия.
        column (int): левая колонка препятствия.
        rows_size (int): высота препятствия.
        columns_size (int): ширина препятствия.
        uid (str): уникальный идентификатор (опционально).
    """

    def __init__(self, row, column, rows_size=1, columns_size=1, uid=None):
        self.row = row
        self.column = column
        self.rows_size = rows_size
        self.columns_size = columns_size
        self.uid = uid

    def get_bounding_box_frame(self):
        """Возвращает строку с рамкой вокруг препятствия (для отладки)."""

        rows, columns = self.rows_size + 1, self.columns_size + 1
        return "\n".join(_get_bounding_box_lines(rows, columns))

    def get_bounding_box_corner_pos(self):
        """Возвращает координаты левого верхнего угла рамки."""

        return self.row - 1, self.column - 1

    def dump_bounding_box(self):
        """Возвращает (row, column, frame) для отрисовки рамки."""

        row, column = self.get_bounding_box_corner_pos()
        return row, column, self.get_bounding_box_frame()

    def has_collision(
        self, obj_corner_row, obj_corner_column, obj_size_rows=1, obj_size_columns=1
    ):
        """Проверяет столкновение с другим объектом.

        Args:
            obj_corner_row (int): строка левого верхнего угла объекта.
            obj_corner_column (int): колонка левого верхнего угла объекта.
            obj_size_rows (int): высота объекта.
            obj_size_columns (int): ширина объекта.

        Returns:
            bool: True, если объекты пересекаются.
        """

        return has_collision(
            (self.row, self.column),
            (self.rows_size, self.columns_size),
            (obj_corner_row, obj_corner_column),
            (obj_size_rows, obj_size_columns),
        )


def _get_bounding_box_lines(rows, columns):
    """Генерирует строки для отрисовки рамки."""

    yield " " + "-" * columns + " "
    for _ in range(rows):
        yield "|" + " " * columns + "|"
    yield " " + "-" * columns + " "


async def show_obstacles(canvas, obstacles):
    """Отображает рамки препятствий (для отладки)."""

    while True:
        boxes = []

        for obstacle in obstacles:
            boxes.append(obstacle.dump_bounding_box())

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame)

        await asyncio.sleep(0)

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame, negative=True)


def _is_point_inside(
    corner_row, corner_column, size_rows, size_columns, point_row, point_row_column
):
    """Проверяет, находится ли точка внутри прямоугольника."""

    rows_flag = corner_row <= point_row < corner_row + size_rows
    columns_flag = corner_column <= point_row_column < corner_column + size_columns

    return rows_flag and columns_flag


def has_collision(obstacle_corner, obstacle_size, obj_corner, obj_size=(1, 1)):
    """Определяет, пересекаются ли два прямоугольника.

    Args:
        obstacle_corner (tuple): (row, col) левого верхнего угла первого.
        obstacle_size (tuple): (rows, cols) размер первого.
        obj_corner (tuple): (row, col) левого верхнего угла второго.
        obj_size (tuple): (rows, cols) размер второго.

    Returns:
        bool: True при пересечении.
    """

    opposite_obstacle_corner = (
        obstacle_corner[0] + obstacle_size[0] - 1,
        obstacle_corner[1] + obstacle_size[1] - 1,
    )

    opposite_obj_corner = (
        obj_corner[0] + obj_size[0] - 1,
        obj_corner[1] + obj_size[1] - 1,
    )

    return any(
        [
            _is_point_inside(*obstacle_corner, *obstacle_size, *obj_corner),
            _is_point_inside(*obstacle_corner, *obstacle_size, *opposite_obj_corner),
            _is_point_inside(*obj_corner, *obj_size, *obstacle_corner),
            _is_point_inside(*obj_corner, *obj_size, *opposite_obstacle_corner),
        ]
    )
