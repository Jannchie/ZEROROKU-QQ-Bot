from nonebot import on_command, rule
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
import random

roll = on_command("roll")


@roll.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    print(args)
    res = random.choice(range(1, 7))
    await roll.finish(f"摇出了 {res}。")
