from .utils import sleep
from .game_scenario import PHRASES


async def update_year(info_win, current_year, year_ticks=15):
    """Обновляет год и выводит информацию в подокне info_win."""
    while True:
        await sleep(year_ticks)
        current_year[0] += 1
        year = current_year[0]

        info_win.clear()
        height, width = info_win.getmaxyx()

        year_str = f"Year: {year}"
        info_win.addstr(1, 2, year_str)

        if year in PHRASES:
            phrase = PHRASES[year]
            max_len = width - 4
            if len(phrase) > max_len:
                phrase = phrase[:max_len]
            info_win.addstr(2, 2, phrase)

        info_win.refresh()
