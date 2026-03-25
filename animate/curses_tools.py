SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258
ESC_KEY_CODE = 27


def read_controls(canvas):
    """Считывает нажатия клавиш за один тик.

    Неблокирующая функция: если клавиша не нажата, возвращает (0,0,False,False).
    Возвращает направление движения по стрелкам, нажатие пробела и ESC.

    Args:
        canvas: curses window объект (должен быть в режиме nodelay).

    Returns:
        tuple: (rows_direction, columns_direction, space_pressed, quit_pressed)
            rows_direction: -1 (вверх), 1 (вниз), 0 (нет движения)
            columns_direction: -1 (влево), 1 (вправо), 0 (нет движения)
            space_pressed: bool, нажат ли пробел
            quit_pressed: bool, нажата ли ESC
    """

    rows_direction = columns_direction = 0
    space_pressed = False
    quit_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

        if pressed_key_code == ESC_KEY_CODE:
            quit_pressed = True
            break

    return rows_direction, columns_direction, space_pressed, quit_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Рисует или стирает многострочный текст на canvas.

    Если negative=False, текст рисуется (пробелы игнорируются).
    Если negative=True, текст стирается (на месте символов ставятся пробелы).

    Args:
        canvas: curses window объект.
        start_row (int): строка начала вывода.
        start_column (int): колонка начала вывода.
        text (str): многострочный текст для отрисовки.
        negative (bool, optional): если True, стирает текст. По умолчанию False.

    Returns:
        None.
    """

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == " ":
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else " "
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Возвращает размер многострочного текста.

    Args:
        text (str): многострочный текст.

    Returns:
        tuple: (rows, columns) — количество строк и максимальную длину строки.
    """

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns
