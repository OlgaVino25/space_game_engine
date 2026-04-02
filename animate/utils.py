import asyncio


async def sleep(tics=1):
    """Приостанавливает корутину на заданное количество тиков."""

    for _ in range(tics):
        await asyncio.sleep(0)
