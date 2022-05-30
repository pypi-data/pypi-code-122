import asyncio
import base64
import os
from datetime import datetime, timedelta
from io import BytesIO

from pathlib import Path
from PIL import Image
from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from playwright._impl._api_types import TimeoutError

from .config import Config
from .._utils import get_browser


ark_daily_config = Config.parse_obj(get_driver().config.dict())
DAILY_LEVELS_PATH = Path(ark_daily_config.daily_levels_path)

async def get_daily_sources(is_force: bool = False):
    """获取每日资源关卡"""
    os.mkdir(DAILY_LEVELS_PATH) if not os.path.exists(DAILY_LEVELS_PATH) else None
    today = str((datetime.now() - timedelta(hours=4)).date())
    file_name = DAILY_LEVELS_PATH / f"{today}.png"
    if file_name.exists() and not is_force:
        return Message(MessageSegment.image(file_name) + f"{today} - 数据来源于 https://prts.wiki/")

    page = None
    for retry in range(3):
        try:
            browser = await get_browser()
            if not browser:
                return None
            url = "https://prts.wiki/"
            page = await browser.new_page()
            await page.goto(url, timeout=10000)
            await page.set_viewport_size({"width": 1920, "height": 1080})
            result = await page.query_selector('div[class="mp-container-left"]')
            await page.wait_for_selector("img", state="visible")
            await result.scroll_into_view_if_needed()
            box = await result.bounding_box()
            box['x'] -= 25
            box['y'] -= 55
            box['width'] -= 130
            box['height'] += 70
            await asyncio.sleep(1)
            screenshot = await page.screenshot(clip=box)
        except TimeoutError:
            logger.warning(f"第{retry + 1}次获取方舟每日资源截图失败……")
            continue
        except AttributeError:
            logger.warning(f"第{retry + 1}次获取方舟每日资源截图失败……")
            continue
        except Exception as e:
            if page:
                await page.close()
            logger.error(f"方舟每日资源截图失败！ - {type(e)}: {e}")
            return None
        else:
            await page.close()
            b_scr = BytesIO(screenshot)
            img = Image.open(b_scr)
            img.save(file_name)
            return Message(
                MessageSegment.image(base64.b64encode(screenshot)) + f"{today} - 数据来源于 https://prts.wiki/")
    if page:
        await page.close()
    return None
