from asyncio import run
from http import cookies
from typing import TYPE_CHECKING
from typing import Union

from src.testers import Logger
from src.tools import request_post

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["TtWid", "TtWidTikTok"]


class TtWid:
    NAME = "ttwid"
    API = "https://ttwid.bytedance.com/ttwid/union/register/"
    DATA = (
        '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":'
        '{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}')

    @classmethod
    async def get_tt_wid(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"], ) -> dict | None:
        if response := await request_post(logger, cls.API, cls.DATA):
            return cls.extract(logger, response, cls.NAME)
        logger.error(f"获取 {cls.NAME} 参数失败！")

    @staticmethod
    def extract(logger: Union["BaseLogger", "LoggerManager", "Logger"],
                headers,
                key: str) -> dict | None:
        if c := headers.get("Set-Cookie"):
            cookie_jar = cookies.SimpleCookie()
            cookie_jar.load(c)
            if v := cookie_jar.get(key):
                return {key: v.value}
        logger.error(f"获取 {key} 参数失败！")


class TtWidTikTok(TtWid):
    pass


async def demo():
    print(await TtWid.get_tt_wid(Logger()))


if __name__ == "__main__":
    run(demo())
