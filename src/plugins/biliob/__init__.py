import asyncio
import random
from nonebot import on_command, rule
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
import aiohttp
from nonebot.log import logger

fans = on_command("fans")

zeroroku_accept = ["06收到。", "06收到请求。", "06已收到请求。"]
zeroroku_searching = ["正在查询中。", "现在正在查询。", "在查了。", "查询中。"]


def select_one(list: list):
    idx = random.randint(0, len(list) - 1)
    return list[idx]


@fans.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    qq = event.get_user_id()
    await asyncio.sleep(random.uniform(2, 4))
    await fans.send(f"{select_one(zeroroku_accept)}{select_one(zeroroku_searching)}")
    await asyncio.sleep(random.uniform(2, 4))
    try:
        mid = str(event.get_message())
    except:
        await fans.finish(f"06娘没能成功解析参数。")
    logger.info(mid)
    url = f"https://api.tokyo.biliob233.com/author/{mid}"
    async with aiohttp.ClientSession() as session:
        res = await session.get(url)
        if res.status == 200:
            try:
                j = await res.json()
            except:
                await fans.finish(f"已获取响应。但是没能成功解析数据。")
            if "name" in j and "cRate" in j:
                await fans.finish(
                    f"已查询到结果。{j['name']} 粉丝数: {j['cFans']}({'+' if j['cRate'] > 0 else '' }{j['cRate']})。"
                )
            else:
                await fans.finish(f"已获取响应。但是没能成功解析数据。")
        await fans.finish(f"收到错误代码：{res.status}。获取数据异常。")
