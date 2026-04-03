import curses


def show_gameover(canvas):
    """Отображает надпись GAME OVER в центре экрана."""
    height, width = canvas.getmaxyx()
    try:
        with open("gameover_art.txt", "r") as f:
            art_lines = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        art_lines = ["GAME OVER"]

    art_height = len(art_lines)
    art_width = max(len(line) for line in art_lines) if art_lines else 0

    if art_height <= height and art_width <= width:
        start_row = (height - art_height) // 2
        start_col = (width - art_width) // 2
        for i, line in enumerate(art_lines):
            try:
                canvas.addstr(start_row + i, start_col, line)
            except curses.error:
                pass
    else:
        msg = "GAME OVER"
        x = (width - len(msg)) // 2
        y = height // 2
        canvas.addstr(y, x, msg)
